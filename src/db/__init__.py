import os
from dotenv import load_dotenv

from sqlalchemy.exc import NoResultFound
from sqlalchemy.ext.asyncio import create_async_engine

from sqlmodel import SQLModel, select
from sqlmodel.ext.asyncio.session import AsyncSession

from src.db.models import DiscordGuild, DiscordGuildMember, DiscordGuildMemberLink

load_dotenv()
SQLALCHEMY_DATABASE_URI = os.getenv("SQLALCHEMY_DATABASE_URI")

import logging

logger = logging.getLogger(__name__)


class BansheeBotDB:
    def __init__(self):
        self.sqlite_file_name = f"{SQLALCHEMY_DATABASE_URI}"
        self.sqlite_url = f"sqlite+aiosqlite:///{self.sqlite_file_name}"
        self.engine = create_async_engine(self.sqlite_url)

    async def start_engine(self):
        async with self.engine.begin() as session:
            await session.run_sync(SQLModel.metadata.create_all)
            logger.debug("DB engine started...")

    async def stop_engine(self):
        await self.engine.dispose()
        logger.debug("...DB engine disposed")

    async def addDiscordGuild(self, discord_guild_id: int, discord_guild_name: str):
        async with AsyncSession(self.engine) as session:
            discord_guild = await session.exec(
                select(DiscordGuild).where(
                    DiscordGuild.discord_guild_id == discord_guild_id
                )
            )
            try:
                discord_guild = discord_guild.one()
                print("Discord guild already exists.")
            except NoResultFound:
                discord_guild = DiscordGuild(
                    discord_guild_id=discord_guild_id,
                    discord_guild_name=discord_guild_name,
                )
                session.add(discord_guild)
                await session.commit()
                await session.refresh(discord_guild)
            except Exception:
                print("Something went wrong with addDiscordGuild")
