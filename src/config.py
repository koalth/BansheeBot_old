from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field


class Config(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    DEBUG: bool = Field(default=False)

    DISCORD_CLIENT_ID: str = Field(default="client_id", init=False)
    DISCORD_TOKEN: str = Field(default="token", init=False)

    API_URL: str = Field(default="api", init=False)


config = Config()
