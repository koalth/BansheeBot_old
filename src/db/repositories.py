from typing import Optional
from sqlalchemy.exc import NoResultFound
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker

from src.db.models import GuildOrm, CharacterOrm
from src.models import GuildDTO, CharacterDTO, Region


import logging

logger = logging.getLogger("Repository")
logger.setLevel(level=logging.DEBUG)
ch = logging.StreamHandler()
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
ch.setFormatter(formatter)
logger.addHandler(ch)


def createCharacterDTOFromOrm(character_orm: CharacterOrm) -> CharacterDTO:
    return CharacterDTO(
        name=character_orm.name,
        realm=character_orm.realm,
        region=Region(character_orm.region),
        discord_user_id=character_orm.discord_user_id,
        item_level=character_orm.item_level,
        class_name=character_orm.class_name,
        profile_url=character_orm.profile_url,
        thumbnail_url=character_orm.thumbnail_url,
        last_crawled_at=character_orm.last_crawled_at,
        guild_id=character_orm.guild_id,
    )


def createGuildDTOFromOrm(guild_orm: GuildOrm) -> GuildDTO:
    return GuildDTO(
        name=guild_orm.name,
        realm=guild_orm.realm,
        region=Region(guild_orm.region),
        discord_guild_id=guild_orm.discord_guild_id,
        characters=[
            createCharacterDTOFromOrm(character) for character in guild_orm.characters
        ],
    )


class GuildRepository:

    @staticmethod
    async def get_by_id(
        async_session: async_sessionmaker[AsyncSession], id: int
    ) -> Optional[GuildDTO]:
        try:
            async with async_session() as session:
                result = (
                    await session.execute(select(GuildOrm).where(GuildOrm.id == id))
                ).scalar_one()

                return createGuildDTOFromOrm(result)
        except NoResultFound:
            logger.error(f"get_by_id Error: No guild with id {id}")
        except Exception as err:
            logger.error(f"get_by_id Error: {err}")

    @staticmethod
    async def get_by_discord_guild_id(
        async_session: async_sessionmaker[AsyncSession], discord_guild_id: int
    ) -> Optional[GuildDTO]:
        try:
            async with async_session() as session:
                result = (
                    await session.execute(
                        select(GuildOrm).where(
                            GuildOrm.discord_guild_id == discord_guild_id
                        )
                    )
                ).scalar_one()

                return createGuildDTOFromOrm(result)

        except NoResultFound:
            logger.error(
                f"get_by_discord_guild_id Error: No guild with discord_guild_id {discord_guild_id}"
            )
        except Exception as err:
            logger.error(f"get_by_discord_guild_id Error: {err}")

    @staticmethod
    async def add(
        async_session: async_sessionmaker[AsyncSession],
        name: str,
        realm: str,
        region: Region,
        discord_guild_id: int,
    ) -> Optional[GuildDTO]:
        try:
            async with async_session() as session:
                # check if guild already exists.
                wow_guild_result = (
                    await session.execute(
                        select(GuildOrm)
                        .where(GuildOrm.name == name)
                        .options(selectinload(GuildOrm.characters))
                    )
                ).scalar_one_or_none()

                if wow_guild_result is not None:
                    logger.debug("Guild already exists")
                    return createGuildDTOFromOrm(wow_guild_result)

                db_wow_guild = GuildOrm(
                    name=name,
                    realm=realm,
                    region=region,
                    discord_guild_id=discord_guild_id,
                    characters=[],
                )

                session.add(db_wow_guild)
                await session.commit()
                await session.refresh(db_wow_guild, ["characters"])

                return createGuildDTOFromOrm(db_wow_guild)

        except Exception as err:
            logger.error(f"add Error: {err}")


class CharacterRepository:

    @staticmethod
    async def get_by_id(
        async_session: async_sessionmaker[AsyncSession], id: int
    ) -> Optional[CharacterDTO]:
        try:
            async with async_session() as session:
                db_character = (
                    await session.execute(
                        select(CharacterOrm).where(CharacterOrm.id == id)
                    )
                ).scalar_one()

                return createCharacterDTOFromOrm(db_character)
        except NoResultFound:
            logger.error(f"get_by_id Error: No character with id {id}")
        except Exception as err:
            logger.error(f"get_by_id Error: {err}")

    @staticmethod
    async def get_by_discord_user_id(
        async_session: async_sessionmaker[AsyncSession], discord_user_id: int
    ) -> Optional[CharacterDTO]:
        try:
            async with async_session() as session:
                db_character = (
                    await session.execute(
                        select(CharacterOrm).where(
                            CharacterOrm.discord_user_id == discord_user_id
                        )
                    )
                ).scalar_one()

                return createCharacterDTOFromOrm(db_character)

        except NoResultFound:
            logger.error(
                f"get_by_discord_user_id Error: No character with discord_user_id {discord_user_id}"
            )
        except Exception as err:
            logger.error(f"get_by_discord_user_id Error: {err}")

    @staticmethod
    async def add(
        async_session: async_sessionmaker[AsyncSession], character: CharacterDTO
    ) -> Optional[CharacterDTO]:
        try:
            async with async_session() as session:
                # check if guild already exists.
                db_character = (
                    await session.execute(
                        select(CharacterOrm).where(CharacterOrm.name == character.name)
                    )
                ).scalar_one_or_none()

                if db_character is not None:
                    logger.debug("Guild already exists")
                    return createCharacterDTOFromOrm(db_character)

                db_wow_character = CharacterOrm(
                    name=character.name,
                    region=character.region,
                    realm=character.realm,
                    discord_user_id=character.discord_user_id,
                )

                session.add(db_wow_character)
                await session.commit()
                await session.refresh(db_wow_character)

                return createCharacterDTOFromOrm(db_wow_character)
        except Exception as err:
            logger.error(f"add Error: {err}")
