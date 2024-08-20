from src.db import IGuildRepository
from src.injector import inject

from typing import Optional
from src.entities import Guild
from src.raiderIO import RaiderIOClient
from sqlalchemy.exc import NoResultFound
from src.mapper import guild_response_to_entity
import logging


class GuildService:

    repository: IGuildRepository = inject.attr(IGuildRepository)

    async def get_by_guild_name_and_realm(
        self, name: str, realm: str
    ) -> Optional[Guild]:
        print(name, realm)
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
