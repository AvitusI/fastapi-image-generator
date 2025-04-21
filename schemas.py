from datetime import datetime
from typing import Dict, Optional

from pydantic import BaseModel, Field


class MessageEvent(BaseModel):
    message: str
    description_id: Optional[str] = Field(None)


class GeneratedImageBase(BaseModel):
    prompt: str
    negative_prompt: Optional[str] = None
    num_steps: int = 50
    description_id: Optional[str] = None


class GeneratedImageCreate(GeneratedImageBase):
    pass


class GeneratedImageRead(GeneratedImageBase):
    id: int
    file_name: Optional[str] = None
    completed: bool
    created_at: datetime

    class Config:
        from_attributes = True


class GeneratedImageURL(BaseModel):
    url: str