from datetime import datetime

from sqlalchemy import Boolean, DateTime, Integer, String, Text, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

class Base(DeclarativeBase):
    pass

class GeneratedImage(Base):
    __tablename__ = "generated_images"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    completed: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    prompt: Mapped[str] = mapped_column(Text, nullable=False)
    negative_prompt: Mapped[str | None] = mapped_column(Text, nullable=True)
    num_steps: Mapped[int] = mapped_column(Integer, nullable=False)
    file_name: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True
    )
    description_id: Mapped[str | None] = mapped_column(String, default=None)

