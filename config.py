from typing import Optional

from pydantic_settings import BaseSettings, SettingsConfigDict


class BaseConfig(BaseSettings):
    DATABASE_URL: Optional[str]
    STORAGE_BUCKET: Optional[str]
    REDIS_URL: Optional[str]
    REDIS_HOST: Optional[str]
    REDIS_PORT: Optional[str]
    REDIS_USERNAME: Optional[str]
    REDIS_PASSWORD: Optional[str]
    REDIS_NAMESPACE: Optional[str]

    model_config = SettingsConfigDict(
        env_file=".env", extra="ignore"
    )
