from typing import Optional, TypeVar
from sqlalchemy.exc import NoResultFound
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy import BinaryExpression

from src.config import Config

from sqlmodel import SQLModel, select
from sqlmodel.ext.asyncio.session import AsyncSession

from src.models import GuildDTO, CharacterDTO

from src.db.models import (
    WowGuild,
    WowCharacter,
)

import logging

logger = logging.getLogger("Database")
logger.setLevel(level=logging.DEBUG)
ch = logging.StreamHandler()
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
ch.setFormatter(formatter)
logger.addHandler(ch)

Model = TypeVar("Model", bound=SQLModel)


class BansheeBotDB:
    def __init__(self, config: Config):
        self.config = config
        self.engine = create_async_engine(self.config.SQLITE_URL)

    async def start_engine(self):
        logger.info("DB engine started...")

    async def stop_engine(self):
        await self.engine.dispose()
        logger.info("...DB engine disposed")

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
        self, discord_guild_id: int, wow_guild: GuildDTO
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
            logger.error("There was a problem creating db_wow_guild: ", err)
            return None

    async def getWowGuild(self, discord_guild_id: int) -> Optional[WowGuild]:
        db_wow_guild = await self.get_one_by_expression(
            WowGuild, WowGuild.discord_guild_id == discord_guild_id
        )

        return db_wow_guild

    async def addWowCharacterToWowGuild(
        self, discord_guild_id: int, character: CharacterDTO, discord_user_id: int
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
                logger.debug("WowGuild not found for current discord server")
                return None
            except Exception as err:
                logger.error("THere was an error adding wow character", err)
                return None
