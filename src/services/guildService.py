from loguru import logger
import inject
from typing import Optional
from src.entities import Guild, GuildCreate, GuildUpdate
from src.external.raiderIO import IRaiderIOClient
from src.db import GuildOrm, IGuildRepository
from sqlalchemy.exc import NoResultFound
from .base import GenericService, IGenericService
from abc import abstractmethod, ABCMeta


class IGuildService(IGenericService[GuildOrm, GuildCreate, GuildUpdate, Guild]):
    @abstractmethod
    async def get_by_discord_guild_id(self, discord_guild_id: str) -> Guild:
        raise NotImplementedError()

    @abstractmethod
    async def does_guild_settings_exist(self, discord_guild_id: str) -> bool:
        raise NotImplementedError()


class GuildService(IGuildService):
    repository: IGuildRepository = inject.attr(IGuildRepository)

    async def get_by_discord_guild_id(self, discord_guild_id: str) -> Guild:
        return await self.repository.get_by_filters(
            GuildOrm.discord_guild_id == discord_guild_id
        )

    async def does_guild_settings_exist(self, discord_guild_id: str) -> bool:
        try:
            return (
                await self.get_by_discord_guild_id(discord_guild_id=discord_guild_id)
                is not None
            )
        except NoResultFound:
            return False
