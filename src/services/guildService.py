from loguru import logger
import inject
from typing import Optional
from src.entities import Guild, GuildCreate, GuildUpdate
from src.external.raiderIO import IRaiderIOClient
from src.db import GuildOrm, IGuildRepository
from .base import GenericService, IGenericService
from abc import abstractmethod, ABCMeta


class IGuildService(
    IGenericService[GuildOrm, GuildCreate, GuildUpdate, Guild], metaclass=ABCMeta
):
    @abstractmethod
    async def get_by_discord_guild_id(self, discord_guild_id: str) -> Guild:
        raise NotImplementedError()


class GuildService(
    IGuildService, GenericService[GuildOrm, GuildCreate, GuildUpdate, Guild]
):
    repository: IGuildRepository = inject.attr(IGuildRepository)

    async def get_by_discord_guild_id(self, discord_guild_id: str) -> Guild:
        return await self.repository.get_by_filters(
            GuildOrm.discord_guild_id == discord_guild_id
        )
