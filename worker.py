import os
from dotenv import load_dotenv
import random
import asyncio
import requests
import websockets
import uuid
import json

import dramatiq
from dramatiq.brokers.redis import RedisBroker
from dramatiq.middleware.middleware import Middleware
from sqlalchemy import select

from text_to_image import TextToImage
from models import GeneratedImage
from database import async_session_maker
from storage import Storage
from config import BaseConfig

load_dotenv()


settings = BaseConfig()

REPLICATE_API_TOKEN = settings.REPLICATE_API_TOKEN


class TextToImageMiddleware(Middleware):
    def __init__(self) -> None:
        super().__init__()
        self.text_to_image = TextToImage()

    def after_process_boot(self, broker):
        self.text_to_image.load_process()
        return super().after_process_boot(broker)
    
text_to_image_middleware = TextToImageMiddleware()

redis_broker = RedisBroker(
    host=settings.REDIS_HOST,
    port=settings.REDIS_PORT,
    username=settings.REDIS_USERNAME,
    password=settings.REDIS_PASSWORD,
    namespace=settings.REDIS_NAMESPACE
)
#redis_broker = RedisBroker(host="localhost", namespace="dramatiq_tasks")
redis_broker.add_middleware(text_to_image_middleware)
dramatiq.set_broker(redis_broker)

def get_image(id: int) -> GeneratedImage:
    async def _get_image(id: int) -> GeneratedImage:
        async with async_session_maker() as session:
            select_query = select(GeneratedImage).where(GeneratedImage.id == id)
            result = await session.execute(select_query)
            image = result.scalar_one_or_none()

            if image is None:
                raise Exception("Image does not exist")
            
            return image
    
    return asyncio.run(_get_image(id))

def update_progress(image: GeneratedImage):
    async def _update_progress(image: GeneratedImage):
        async with async_session_maker() as session:
            image.completed = True
            session.add(image)
            await session.commit()

    asyncio.run(_update_progress(image))

def update_file_name(image: GeneratedImage, file_name: str):
    async def _update_file_name(image: GeneratedImage, file_name: str):
        async with async_session_maker() as session:
            image.file_name = file_name
            session.add(image)
            await session.commit()

    asyncio.run(_update_file_name(image, file_name))

def send_image_message(message: str, description_id: str = None):
    async def _send_image_message(message: str, description_id: str = None):
        # uri = "wss://https://fastapi-image-generator.onrender.com/ws"
        uri = "ws://localhost:8000/ws"
        async with websockets.connect(uri) as websocket:
            # Create a JSON message with both the image URL and description_id
            json_message = json.dumps({
                "message": message,
                "description_id": description_id
            })
            await websocket.send(json_message)
            print("Message sent from send image coroutine worker")

    asyncio.run(_send_image_message(message, description_id))


@dramatiq.actor()
def text_to_image_task(image_id: int):
    image = get_image(image_id)

    print('from dramatiq actor', image.prompt)

    image_bytes = text_to_image_middleware.text_to_image.generate(
        image.prompt,
        negative_prompt=image.negative_prompt,
        num_steps=image.num_steps
    )

    print(image_bytes)

    if image_bytes is None:
        raise Exception("Image generaion failed")
    
    # some models return image url instead of bytes

    file_name = f"{uuid.uuid4()}.jpg"

    storage = Storage()
    storage.upload_image_bytes_to_s3(
        image_bytes,
        settings.STORAGE_BUCKET,
        file_name
    )

    update_file_name(image, file_name)

    update_progress(image)

    result = { 'data': 'great' }
   # webhook_url = "https://fastapi-image-generator.onrender.com/webhook"
    webhook_url = "http://localhost:8000/webhook"

    requests.post(webhook_url, json=result)

    # Send the image URL with the description_id
    send_image_message(
       # f"https://s3.us-west-2.amazonaws.com/avytechs.generated-images/{file_name}", 
        f"https://avitus-web-storage.s3.us-east-1.amazonaws.com/{file_name}",
        image.description_id
    )

    # https://s3.us-west-2.amazonaws.com/avytechs.generated-images/b2eb116a-7d6d-4e03-91af-47b332792f97.jpg


