import asyncio
import logging
from sqlalchemy.ext.asyncio import create_async_engine
import os
from dotenv import load_dotenv
from src.db.models import Base

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
        await connection.run_sync(Base.metadata.create_all)

    await engine.dispose()
    logger.info("...Migration completed")


async def destroy_tables() -> None:
    logger.info("Starting to destroy tables...")

    sqlite_file_name = f"{SQLALCHEMY_DATABASE_URI}"
    sqlite_url = f"sqlite+aiosqlite:///{sqlite_file_name}"

    engine = create_async_engine(sqlite_url)
    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.drop_all)

    await engine.dispose()
    logger.info("...Destruction completed")


async def reset_tables() -> None:
    logger.info("Starting to reset tables...")
    await destroy_tables()
    await migrate_tables()
    logger.info("...Resetting completed")


def migrate():
    asyncio.run(migrate_tables())


def destroy():
    asyncio.run(destroy_tables())


def reset():
    asyncio.run(reset_tables())
