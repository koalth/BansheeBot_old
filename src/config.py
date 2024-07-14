import os
from dotenv import load_dotenv

load_dotenv()


class ConfigError(Exception):
    pass


class Config:
    DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
    DISCORD_CLIENT_ID = os.getenv("DISCORD_CLIENT_ID")

    # Database
    SQLALCHEMY_DATABASE_URI = os.getenv("SQLALCHEMY_DATABASE_URI")
    SQLITE_URL = f"sqlite+aiosqlite:///{SQLALCHEMY_DATABASE_URI}"

    def __init__(self):

        if self.DISCORD_TOKEN is None:
            raise ConfigError("DISCORD_TOKEN not defined")

        if self.SQLALCHEMY_DATABASE_URI is None:
            raise ConfigError("SQLALCHEMY_DATABASE_URI not defined")