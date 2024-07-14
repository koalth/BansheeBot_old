from typing import Optional, TypeVar
from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import selectinload
from sqlalchemy import select, inspect
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession

from src.config import Config

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


class BansheeBotDB:
    def __init__(self, config: Config):
        self.config = config
        self.engine = create_async_engine(self.config.SQLITE_URL)

    async def start_engine(self):
        logger.info("DB engine started...")

    async def stop_engine(self):
        await self.engine.dispose()
        logger.info("...DB engine disposed")

    async def addWowGuild(
        self, discord_guild_id: int, wow_guild: GuildDTO
    ) -> Optional[WowGuild]:
        async with AsyncSession(self.engine) as session:
            try:

                result = (
                    await session.execute(
                        select(WowGuild).where(
                            WowGuild.discord_guild_id == discord_guild_id
                        )
                    )
                ).scalar_one_or_none()

                if result is not None:
                    return result

                db_wow_guild = WowGuild(
                    name=wow_guild.name,
                    region=wow_guild.region,
                    realm=wow_guild.realm,
                    discord_guild_id=discord_guild_id,
                )

                session.add(db_wow_guild)
                await session.commit()
                await session.refresh(db_wow_guild)
                return db_wow_guild
            except Exception as err:
                logger.error("There was a problem creating db_wow_guild: ", err)
                return None

    async def getWowGuild(self, discord_guild_id: int) -> Optional[WowGuild]:
        async with AsyncSession(self.engine) as session:
            try:
                db_wow_guild = (
                    await session.execute(
                        select(WowGuild).where(
                            WowGuild.discord_guild_id == discord_guild_id
                        )
                    )
                ).scalar_one()

                return db_wow_guild
            except NoResultFound:
                logger.debug("WowGuild not found for current discord server")
                return None
            except Exception as err:
                logger.error("THere was an error adding wow character", err)
                return None

    async def addWowCharacterToWowGuild(
        self, discord_guild_id: int, character: CharacterDTO, discord_user_id: int
    ) -> Optional[WowCharacter]:
        async with AsyncSession(self.engine) as session:
            try:

                # check if char is already in the guild
                wow_character_result = (
                    await session.execute(
                        select(WowCharacter).where(WowCharacter.name == character.name)
                    )
                ).scalar_one_or_none()

                if wow_character_result is not None:
                    raise Exception("Character already exists in Guild")

                db_wow_guild = (
                    await session.execute(
                        select(WowGuild).where(
                            WowGuild.discord_guild_id == discord_guild_id
                        )
                    )
                ).scalar_one()

                session.add(db_wow_guild)
                logger.debug(db_wow_guild)

                db_wow_character = WowCharacter(
                    **character.model_dump(
                        include={
                            "name",
                            "region",
                            "realm",
                            "thumbnail_url",
                            "item_level",
                            "last_crawled_at",
                        }
                    ),
                    discord_user_id=discord_user_id,
                    wow_guild_id=db_wow_guild.id
                )

                session.add(db_wow_character)
                await session.commit()
                await session.refresh(db_wow_character, ["wow_guild"])

                return db_wow_character
            except NoResultFound:
                logger.debug("WowGuild not found for current discord server")
                return None
            except Exception as err:
                logger.error("THere was an error adding wow character", err)
                return None
