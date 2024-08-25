from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field


class Config(BaseSettings):
    model_config = SettingsConfigDict(
        env_file="dev.env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    DEBUG: bool = Field(default=False)

    DISCORD_CLIENT_ID: str = Field(init=False)
    DISCORD_TOKEN: str = Field(init=False)

    API_URL: str = Field(init=False)


config = Config()
