from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field, computed_field, field_validator, ValidationInfo
from typing import Optional

class Config(BaseSettings):
    model_config = SettingsConfigDict(
        env_file="dev.env", env_file_encoding="utf-8", extra="ignore"
    )

    DEBUG: bool = Field(default=False)

    DISCORD_TOKEN: str = Field(default="")
    DISCORD_CLIENT_ID: str = Field(default="")

    SQLALCHEMY_DATABASE_URI: str = Field(default="")

    POSTGRES_USER: str = Field(default="")
    POSTGRES_PASSWORD: str = Field(default="")
    POSTGRES_HOST: str = Field(default="")
    POSTGRES_PORT: str = Field(default="")
    DATABASE_URL: str = Field(default=None)

    @field_validator("DATABASE_URL", mode="before")
    @classmethod
    def assemble_db_url(cls, v: Optional[str], values: ValidationInfo) -> str:
        if v is None:
            return f"postgresql+asyncpg://{values.data['POSTGRES_USER']}:{values.data['POSTGRES_PASSWORD']}@{values.data['POSTGRES_HOST']}:{values.data['POSTGRES_PORT']}"
        return v

    API_URL: str = Field(default="")
    CALLS: int = Field(default=0)
    RATE_LIMIT: int = Field(default=0)
    TIMEOUT: int = Field(default=0)
    RETRIES: int = Field(default=0)
    BACKOFF_FACTOR: int = Field(default=0)


config = Config()
