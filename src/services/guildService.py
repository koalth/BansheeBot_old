from loguru import logger
import inject
from typing import Optional
from src.entities import Guild, GuildCreate
from src.raiderIO import IRaiderIOClient
from src.db import GuildRepository
from abc import abstractmethod, ABCMeta


class IGuildService(metaclass=ABCMeta):

    @abstractmethod
    async def get_by_discord_guild_id(self, discord_guild_id: str) -> Optional[Guild]:
        raise NotImplementedError()

    @abstractmethod
    async def create_guild(
        self, name: str, realm: str, region: str, discord_guild_id: str
    ) -> Optional[Guild]:
        raise NotImplementedError()


class GuildService(IGuildService):

    guildRepository: GuildRepository = inject.attr(GuildRepository)
    raiderIOClient: IRaiderIOClient = inject.attr(IRaiderIOClient)

    async def get_by_discord_guild_id(self, discord_guild_id: str) -> Optional[Guild]:
        return await self.guildRepository.get_by_discord_guild_id(discord_guild_id)

    async def create_guild(
        self, name: str, realm: str, region: str, discord_guild_id: str
    ) -> Optional[Guild]:

        guild_io = await self.raiderIOClient.getGuildProfile(name, realm, region)

        logger.debug(f"guild io: {guild_io}")

        if guild_io is None:
            return None

        guild_ent = GuildCreate(
            name=guild_io.name,
            realm=guild_io.realm,
            region=guild_io.region,
            item_level_requirement=None,
            discord_guild_id=discord_guild_id,
        )
        return await self.guildRepository.add_guild(guild_ent)
