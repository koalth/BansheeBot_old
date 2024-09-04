import os
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field, field_validator, ValidationInfo
from typing import Optional


class Config(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=f".env.{os.getenv('BOT_ENV', 'dev')}",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    DEBUG: bool = Field(default=False)

    DISCORD_CLIENT_ID: str = Field(default="client_id", init=False)
    DISCORD_TOKEN: str = Field(default="token", init=False)

    API_URL: str = Field(default="api", init=False)

    POSTGRES_USER: str = Field(default="admin", init=False)
    POSTGRES_PASSWORD: str = Field(default="password")
    POSTGRES_HOST: str = Field(default="localhost")
    POSTGRES_PORT: int = Field(default=5432)
    DATABASE_URL: str = Field(default=None)

    @field_validator("DATABASE_URL", mode="before")
    @classmethod
    def assemble_db_url(cls, v: Optional[str], values: ValidationInfo) -> str:
        if v is None:
            return f"postgresql+asyncpg://{values.data['POSTGRES_USER']}:{values.data['POSTGRES_PASSWORD']}@{values.data['POSTGRES_HOST']}:{values.data['POSTGRES_PORT']}"
        return v


config = Config()
