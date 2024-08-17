from typing import Optional
from src.entities import Guild
from src.db import GuildRepository
from src.raiderIO import RaiderIOClient
import logging
from sqlalchemy.exc import NoResultFound

logger = logging.getLogger("GuildService")
logger.setLevel(level=logging.DEBUG)
ch = logging.StreamHandler()
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
ch.setFormatter(formatter)
logger.addHandler(ch)

from src.mapper import guild_response_to_entity, character_response_to_entity


class GuildService:

    repository: GuildRepository

    def __init__(self, repository: GuildRepository = GuildRepository()):
        self.repository = repository

    async def get_by_guild_name_and_realm(
        self, name: str, realm: str
    ) -> Optional[Guild]:
        return await self.repository.get_by_guild_name_and_realm(name, realm)

    async def get_by_discord_guild_id(self, discord_guild_id: int) -> Optional[Guild]:
        return await self.repository.get_by_discord_guild_id(discord_guild_id)

    async def add_wow_guild(
        self, name: str, realm: str, region: str, discord_guild_id: int
    ) -> Optional[Guild]:

        guild_io = await RaiderIOClient.getGuildProfile(name, realm, region)

        if guild_io is None:
            raise Exception("guild io was None")

        guild_entity = guild_response_to_entity(guild_io)
        guild_entity.discord_guild_id = discord_guild_id

        guild_db = await self.repository.add(guild_entity)

        return guild_db

    async def is_discord_already_linked(self, guild_id: int) -> bool:
        try:
            return (await self.get_by_discord_guild_id(guild_id)) is not None
        except NoResultFound:
            return False

    async def is_wow_guild_already_linked(self, name: str, realm: str) -> bool:
        try:
            return (await self.get_by_guild_name_and_realm(name, realm)) is not None
        except NoResultFound:
            return False
