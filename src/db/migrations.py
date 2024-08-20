import asyncio
from loguru import logger
from sqlalchemy.ext.asyncio import create_async_engine
from src.config import Config
from src.db.models import Base


async def migrate_tables() -> None:
    logger.info("Starting to migrate...")

    engine = create_async_engine(Config.SQLITE_URL)
    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.create_all)

    await engine.dispose()
    logger.info("...Migration completed")


async def destroy_tables() -> None:
    logger.info("Starting to destroy tables...")

    engine = create_async_engine(Config.SQLITE_URL)
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
