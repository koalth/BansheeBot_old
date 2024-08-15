from typing import Optional
from sqlalchemy.exc import NoResultFound
from sqlalchemy import select
from sqlalchemy.orm import selectinload


from src.db.database import get_session
from src.db.models import GuildOrm, CharacterOrm


import logging

logger = logging.getLogger("Repository")
logger.setLevel(level=logging.DEBUG)
ch = logging.StreamHandler()
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
ch.setFormatter(formatter)
logger.addHandler(ch)


class GuildRepository:

    def __init__(self):
        pass

    async def get_by_discord_guild_id(self, id: int) -> GuildOrm:
        try:
            async with get_session() as session:
                result = (
                    await session.execute(
                        select(GuildOrm).where(GuildOrm.discord_guild_id == id)
                    )
                ).scalar_one()

                return result
        except Exception as err:
            logger.error(f"get_by_discord_guild_id error: {err}")
            raise err

    async def create_guild(
        self,
        name: str,
        realm: str,
        region: str,
        discord_guild_id: int,
    ) -> GuildOrm:
        try:
            async with get_session() as session:
                db_wow_guild = GuildOrm(
                    name=name,
                    realm=realm,
                    region=region,
                    discord_guild_id=discord_guild_id,
                )

                session.add(db_wow_guild)
                await session.commit()
                await session.refresh(db_wow_guild)

                return db_wow_guild
        except Exception as err:
            raise err


# class GuildRepository:

#     @staticmethod
#     async def get_by_id(
#         async_session: async_sessionmaker[AsyncSession], id: int
#     ) -> Optional[GuildOrm]:
#         try:
#             async with async_session() as session:
#                 result = (
#                     await session.execute(select(GuildOrm).where(GuildOrm.id == id))
#                 ).scalar_one()

#                 return result
#         except NoResultFound:
#             logger.error(f"get_by_id Error: No guild with id {id}")
#         except Exception as err:
#             logger.error(f"get_by_id Error: {err}")

#     @staticmethod
#     async def get_by_discord_guild_id(
#         async_session: async_sessionmaker[AsyncSession], discord_guild_id: int
#     ) -> Optional[GuildOrm]:
#         try:
#             async with async_session() as session:
#                 result = (
#                     await session.execute(
#                         select(GuildOrm)
#                         .where(GuildOrm.discord_guild_id == discord_guild_id)
#                         .options(selectinload(GuildOrm.characters))
#                     )
#                 ).scalar_one()

#                 return result

#         except NoResultFound:
#             logger.error(
#                 f"get_by_discord_guild_id Error: No guild with discord_guild_id {discord_guild_id}"
#             )
#         except Exception as err:
#             logger.error(f"get_by_discord_guild_id Error: {err}")

#     @staticmethod
#     async def add(
#         name: str,
#         realm: str,
#         region: Region,
#         discord_guild_id: int,
#     ) -> Optional[GuildOrm]:
#         try:
#             async_session = async_sessionmaker(self.engine, expire_on_commit=False)
#             async with async_session() as session:
#                 # check if guild already exists.
#                 wow_guild_result = (
#                     await session.execute(
#                         select(GuildOrm)
#                         .where(GuildOrm.name == name)
#                         .options(selectinload(GuildOrm.characters))
#                     )
#                 ).scalar_one_or_none()

#                 if wow_guild_result is not None:
#                     logger.debug("Guild already exists")
#                     return wow_guild_result

#                 db_wow_guild = GuildOrm(
#                     name=name,
#                     realm=realm,
#                     region=region,
#                     discord_guild_id=discord_guild_id,
#                     characters=[],
#                 )

#                 session.add(db_wow_guild)
#                 await session.commit()
#                 await session.refresh(db_wow_guild, ["characters"])

#                 return db_wow_guild

#         except Exception as err:
#             logger.error(f"add Error: {err}")


# class CharacterRepository:

#     @staticmethod
#     async def get_by_id(
#         async_session: async_sessionmaker[AsyncSession], id: int
#     ) -> Optional[CharacterDTO]:
#         try:
#             async with async_session() as session:
#                 db_character = (
#                     await session.execute(
#                         select(CharacterOrm).where(CharacterOrm.id == id)
#                     )
#                 ).scalar_one()

#                 return createCharacterDTOFromOrm(db_character)
#         except NoResultFound:
#             logger.error(f"get_by_id Error: No character with id {id}")
#         except Exception as err:
#             logger.error(f"get_by_id Error: {err}")

#     @staticmethod
#     async def get_by_discord_user_id(
#         async_session: async_sessionmaker[AsyncSession], discord_user_id: int
#     ) -> Optional[CharacterDTO]:
#         try:
#             async with async_session() as session:
#                 db_character = (
#                     await session.execute(
#                         select(CharacterOrm).where(
#                             CharacterOrm.discord_user_id == discord_user_id
#                         )
#                     )
#                 ).scalar_one()

#                 return createCharacterDTOFromOrm(db_character)

#         except NoResultFound:
#             logger.error(
#                 f"get_by_discord_user_id Error: No character with discord_user_id {discord_user_id}"
#             )
#         except Exception as err:
#             logger.error(f"get_by_discord_user_id Error: {err}")

#     @staticmethod
#     async def add(
#         async_session: async_sessionmaker[AsyncSession],
#         character: CharacterDTO,
#     ) -> Optional[CharacterDTO]:
#         try:
#             async with async_session() as session:

#                 db_character = (
#                     await session.execute(
#                         select(CharacterOrm).where(CharacterOrm.name == character.name)
#                     )
#                 ).scalar_one_or_none()

#                 if db_character is not None:
#                     logger.debug("character already exists")
#                     return createCharacterDTOFromOrm(db_character)

#                 db_wow_character = CharacterOrm(
#                     name=character.name,
#                     region=character.region,
#                     realm=character.realm,
#                     item_level=character.item_level,
#                     class_name=character.class_name,
#                     profile_url=character.profile_url,
#                     thumbnail_url=character.thumbnail_url,
#                     last_crawled_at=character.last_crawled_at,
#                     discord_user_id=character.discord_user_id,
#                     guild_id=character.guild_id,
#                 )

#                 session.add(db_wow_character)
#                 await session.commit()
#                 await session.refresh(db_wow_character)

#                 return createCharacterDTOFromOrm(db_wow_character)
#         except Exception as err:
#             logger.error(f"add Error: {err}")
