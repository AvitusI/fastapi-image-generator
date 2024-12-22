import asyncio
import contextlib
import json
import os
from dotenv import load_dotenv

from broadcaster import Broadcast
from dramatiq import Message
from fastapi import FastAPI, status, Depends, HTTPException, Request, WebSocket
from starlette.websockets import WebSocketDisconnect
from pydantic import BaseModel, Field, UUID4
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.middleware.cors import CORSMiddleware

import worker as worker
import schemas as schemas
from database import get_async_session, create_all_tables
from models import GeneratedImage
from schemas import MessageEvent
from config import BaseConfig

settings = BaseConfig()

# broadcast = Broadcast("redis://localhost:6379")
broadcast = Broadcast(
    settings.REDIS_URL
)
CHANNEL = "CHAT"

@contextlib.asynccontextmanager
async def lifespan(app: FastAPI):
    await create_all_tables()
    yield

@contextlib.asynccontextmanager
async def lifespan2(app: FastAPI):
    await broadcast.connect()
    yield
    await broadcast.disconnect()

@contextlib.asynccontextmanager
async def combined_lifespan(app: FastAPI):
    async with lifespan(app):
        async with lifespan2(app):
            yield

class ImageGenerationInput(BaseModel):
    prompt: str
    negative_prompt: str | None = Field(None)
    num_steps: int = Field(50, gt=0, le=50)

class ImageGenerationOutput(BaseModel):
    task_id: UUID4 | str

app = FastAPI(lifespan=combined_lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

async def get_generated_image_or_404(
    id: int, 
    session: AsyncSession = Depends(get_async_session)
) -> GeneratedImage:
    select_query = select(GeneratedImage).where(GeneratedImage.id == id)
    result = await session.execute(select_query)
    image = result.scalar_one_or_none()

    if image is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    return image

@app.post(
    "/generated-images",
    response_model=schemas.GeneratedImageRead,
    status_code=status.HTTP_201_CREATED
)
async def create_generated_image(
    generated_image_create: schemas.GeneratedImageCreate,
    session: AsyncSession = Depends(get_async_session)
) -> GeneratedImage:
    image = GeneratedImage(**generated_image_create.model_dump())
    session.add(image)
    await session.commit()

    worker.text_to_image_task.send(image.id)

    return image

# check if the generation is done
@app.get(
    "/generated-images/{id}",
    response_model=schemas.GeneratedImageRead
)
async def get_generated_image(
    image: GeneratedImage = Depends(get_generated_image_or_404)
) -> GeneratedImage:
    return image

@app.post("/webhook")
async def webhook_handler(request: Request):
    payload = await request.json()

    print("From webhook, image generation completed")
    return {"message": "Webhook received successfully"}

async def receive_message(websocket: WebSocket):
    print("Inside receiver")
    async with broadcast.subscribe(channel=CHANNEL) as subscriber:
        async for event in subscriber:
            message_event = MessageEvent.model_validate_json(event.message)
            await websocket.send_json(message_event.model_dump())

async def send_message(websocket: WebSocket):
    print("Inside sender")
    data = await websocket.receive_text()
    event = MessageEvent(message=data)
    await broadcast.publish(channel=CHANNEL, message=event.model_dump_json())


@app.websocket("/ws")
async def image_completion_notify(websocket: WebSocket):
    await websocket.accept()

    try:
        while True:
            receive_message_task = asyncio.create_task(
                receive_message(websocket)
            )
            send_message_task = asyncio.create_task(
                send_message(websocket)
            )

            done, pending = await asyncio.wait(
                { receive_message_task, send_message_task },
                return_when=asyncio.FIRST_COMPLETED
            )

            for task in pending:
                task.cancel()
            for task in done:
                task.result()

    except WebSocketDisconnect:
        pass
