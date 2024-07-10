import os
from dotenv import load_dotenv
from typing import Optional, TypeVar, Generic
from sqlalchemy.exc import NoResultFound
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy import BinaryExpression

import discord

from sqlmodel import SQLModel, select
from sqlmodel.ext.asyncio.session import AsyncSession

from src.raiderIO.models.guild import Guild
from src.raiderIO.models.character import Character

from src.db.entity import (
    WowGuild,
    WowCharacter,
)

load_dotenv()
SQLALCHEMY_DATABASE_URI = os.getenv("SQLALCHEMY_DATABASE_URI")

import logging

logger = logging.getLogger("Database")

Model = TypeVar("Model", bound=SQLModel)


class BansheeBotDB:
    def __init__(self):
        self.sqlite_file_name = f"{SQLALCHEMY_DATABASE_URI}"
        self.sqlite_url = f"sqlite+aiosqlite:///{self.sqlite_file_name}"
        self.engine = create_async_engine(self.sqlite_url)

    async def start_engine(self):
        # async with self.engine.begin() as session:
        # await session.run_sync(SQLModel.metadata.drop_all)
        # await session.run_sync(SQLModel.metadata.create_all)
        logger.debug("DB engine started...")

    async def stop_engine(self):
        await self.engine.dispose()
        logger.debug("...DB engine disposed")

    async def get(self, model: type[Model], id: int) -> Optional[Model]:
        async with AsyncSession(self.engine) as session:
            return await session.get(model, id)

    async def get_one_by_expression(
        self, model: type[Model], *expression: BinaryExpression
    ) -> Optional[Model]:
        async with AsyncSession(self.engine) as session:
            query = select(model)
            if expression:
                query = query.where(*expression)
            return await session.scalar(query)

    async def create(self, model: type[Model]) -> Model:
        async with AsyncSession(self.engine) as session:
            instance = model
            session.add(instance)
            await session.commit()
            await session.refresh(instance)
            return instance

    async def addWowGuild(
        self, discord_guild_id: int, wow_guild: Guild
    ) -> Optional[WowGuild]:

        try:
            db_wow_guild = WowGuild(
                wow_guild_name=wow_guild.name,
                realm=wow_guild.realm,
                region=wow_guild.region,
                discord_guild_id=discord_guild_id,
            )

            db_wow_guild = await self.create(db_wow_guild)

            return db_wow_guild
        except Exception as err:
            print("THere was a problem creating db_wow_guild: ", err)
            return None

    async def getWowGuild(self, discord_guild_id: int) -> Optional[WowGuild]:

        db_wow_guild = await self.get_one_by_expression(
            WowGuild, WowGuild.discord_guild_id == discord_guild_id
        )

        print("getWowGuild: ", db_wow_guild)

        return db_wow_guild

        # async with AsyncSession(self.engine) as session:

        #     db_wow_guild = await session.exec(
        #         select(WowGuild).where(WowGuild.discord_guild_id == discord_guild_id)
        #     )
        #     try:
        #         db_wow_guild = db_wow_guild.unique().one()

        #         return db_wow_guild
        #     except NoResultFound:
        #         print("WowGuild not found for current discord server")
        #         return None

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
