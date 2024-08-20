from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field, computed_field


class Config(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", extra="ignore"
    )

    DEBUG: bool = Field(default=False)

    DISCORD_TOKEN: str = Field(default="")
    DISCORD_CLIENT_ID: str = Field(default="")

    SQLALCHEMY_DATABASE_URI: str = Field(default="")

    @property
    @computed_field
    def SQLITE_URL(self) -> str:
        return f"sqlite+aiosqlite:///{self.SQLALCHEMY_DATABASE_URI}"

    API_URL: str = Field(default="")
    CALLS: int = Field(default=0)
    RATE_LIMIT: int = Field(default=0)
    TIMEOUT: int = Field(default=0)
    RETRIES: int = Field(default=0)
    BACKOFF_FACTOR: int = Field(default=0)


config = Config()
