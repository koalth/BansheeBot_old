import os
from dotenv import load_dotenv
from typing import Optional
from sqlalchemy.exc import NoResultFound
from sqlalchemy.ext.asyncio import create_async_engine

import discord

from sqlmodel import SQLModel, select
from sqlmodel.ext.asyncio.session import AsyncSession

from src.raiderIO.models.guild import Guild
from src.raiderIO.models.character import Character

from src.db.models import (
    DiscordGuild,
    WowGuild,
    WowCharacter,
)

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
            # await session.run_sync(SQLModel.metadata.drop_all)
            await session.run_sync(SQLModel.metadata.create_all)
            logger.debug("DB engine started...")

    async def stop_engine(self):
        await self.engine.dispose()
        logger.debug("...DB engine disposed")

    async def addDiscordGuild(
        self, discord_guild_id: int, discord_guild_name: str
    ) -> Optional[DiscordGuild]:
        async with AsyncSession(self.engine) as session:
            discord_guild = await session.exec(
                select(DiscordGuild).where(
                    DiscordGuild.discord_guild_id == discord_guild_id
                )
            )
            try:
                discord_guild = discord_guild.one()
                print("Discord guild already exists.")
                return discord_guild
            except NoResultFound:
                discord_guild = DiscordGuild(
                    discord_guild_id=discord_guild_id,
                    discord_guild_name=discord_guild_name,
                )
                session.add(discord_guild)
                await session.commit()
                await session.refresh(discord_guild)

                return discord_guild
            except Exception:
                print("Something went wrong with addDiscordGuild")
                return None

    async def addWowGuildToDiscordGuild(
        self, discord_guild_id: int, discord_guild_name: str, wow_guild: Guild
    ) -> Optional[WowGuild]:
        async with AsyncSession(self.engine) as session:
            db_discord_guild = await session.exec(
                select(DiscordGuild).where(
                    DiscordGuild.discord_guild_id == discord_guild_id
                )
            )

            print("discord_ugild_id: ", discord_guild_id)

            try:
                db_discord_guild = db_discord_guild.one()

                print(db_discord_guild)

                db_wow_guild = WowGuild(
                    wow_guild_name=wow_guild.name,
                    realm=wow_guild.realm,
                    region=wow_guild.region,
                    discord_guild=db_discord_guild,
                )

                session.add(db_wow_guild)
                await session.commit()

                await session.refresh(db_wow_guild)

                print(db_wow_guild)
                return db_wow_guild
            except NoResultFound:
                print("Discord guild not found, creating discord guild now..")
                db_discord_guild = await self.addDiscordGuild(
                    discord_guild_id=discord_guild_id,
                    discord_guild_name=discord_guild_name,
                )

                if db_discord_guild is None:
                    raise Exception

                db_wow_guild = WowGuild(
                    wow_guild_name=wow_guild.name,
                    realm=wow_guild.realm,
                    region=wow_guild.region,
                    discord_guild=db_discord_guild,
                    discord_guild_id=db_discord_guild.discord_guild_id,
                )
                session.add(db_wow_guild)
                await session.commit()

                await session.refresh(db_wow_guild)

                return db_wow_guild
            except Exception as err:
                print("Something went wrong with addWowGuildToDiscordGuild: ", err)
                return None

    async def getWowGuild(self, discord_guild_id: int) -> Optional[WowGuild]:
        async with AsyncSession(self.engine) as session:

            db_wow_guild = await session.exec(
                select(WowGuild).where(WowGuild.discord_guild_id == discord_guild_id)
            )
            try:
                db_wow_guild = db_wow_guild.unique().one()

                return db_wow_guild
            except NoResultFound:
                print("WowGuild not found for current discord server")
                return None

    async def addWowCharacterToWowGuild(
        self, discord_guild_id: int, character: Character, discord_user_id: int
    ) -> Optional[WowCharacter]:
        print("discord_guild_id: ", discord_guild_id)
        async with AsyncSession(self.engine) as session:
            db_wow_guild = await session.exec(
                select(WowGuild).where(WowGuild.discord_guild_id == discord_guild_id)
            )
            try:
                db_wow_guild = db_wow_guild.unique().one()

                db_wow_character = WowCharacter(
                    wow_character_name=character.name,
                    region=character.region,
                    realm=character.realm,
                    discord_user_id=discord_user_id,
                    thumbnail_url=character.thumbnail_url,
                    item_level=character.gear.item_level_equipped,
                    wow_guild=db_wow_guild,
                )

                session.add(db_wow_character)
                await session.commit()
                await session.refresh(db_wow_character)

                return db_wow_character
            except NoResultFound:
                print("WowGuild not found for current discord server")
                return None
            except Exception as err:
                print("THere was an error adding wow character", err)
                return None
