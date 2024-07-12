import asyncio
import logging
from sqlalchemy.ext.asyncio import create_async_engine
import os
from sqlmodel import SQLModel
from dotenv import load_dotenv

logger = logging.getLogger("Migrations")
logger.setLevel(level=logging.DEBUG)
ch = logging.StreamHandler()
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
ch.setFormatter(formatter)
logger.addHandler(ch)

load_dotenv()
SQLALCHEMY_DATABASE_URI = os.getenv("SQLALCHEMY_DATABASE_URI")


async def migrate_tables() -> None:
    logger.info("Starting to migrate...")

    sqlite_file_name = f"{SQLALCHEMY_DATABASE_URI}"
    sqlite_url = f"sqlite+aiosqlite:///{sqlite_file_name}"

    engine = create_async_engine(sqlite_url)
    async with engine.begin() as connection:
        await connection.run_sync(SQLModel.metadata.create_all)

    logger.info("...Migration completed")


async def destroy_tables() -> None:
    logger.info("Starting to destroy tables...")

    sqlite_file_name = f"{SQLALCHEMY_DATABASE_URI}"
    sqlite_url = f"sqlite+aiosqlite:///{sqlite_file_name}"

    engine = create_async_engine(sqlite_url)
    async with engine.begin() as connection:
        await connection.run_sync(SQLModel.metadata.drop_all)

    logger.info("...Destruction completed")


def migrate():
    asyncio.run(migrate_tables())


def destroy():
    asyncio.run(destroy_tables())
