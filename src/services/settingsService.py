from typing import Optional, List, Tuple
from src.db import ISettingRepository, SettingOrm
from src.entities import Setting, SettingCreate, SettingUpdate
from .base import GenericService, IGenericService
from sqlalchemy.exc import NoResultFound
from abc import ABC, abstractmethod, ABCMeta
import inject


class ISettingService(
    IGenericService[SettingOrm, SettingCreate, SettingUpdate, Setting]
):
    @abstractmethod
    async def get_by_discord_guild_id(self, discord_guild_id: str) -> Setting:
        raise NotImplementedError()

    @abstractmethod
    async def does_guild_settings_exist(self, discord_guild_id: str) -> bool:
        raise NotImplementedError()

    @abstractmethod
    async def setup_guild_settings(self, discord_guild_id: str) -> Setting:
        raise NotImplementedError()


class SettingService(ISettingService):
    repository: ISettingRepository = inject.attr(ISettingRepository)

    async def get_by_discord_guild_id(self, discord_guild_id: str) -> Setting:
        return await self.repository.get_by_filters(
            SettingOrm.discord_guild_id == discord_guild_id
        )

    async def does_guild_settings_exist(self, discord_guild_id: str) -> bool:
        try:
            return (
                await self.get_by_discord_guild_id(discord_guild_id=discord_guild_id)
                is not None
            )
        except NoResultFound:
            return False

    async def setup_guild_settings(self, discord_guild_id: str) -> Setting:
        obj = SettingCreate(
            discord_guild_id=discord_guild_id,
            default_realm=None,
            default_region=None,
            raider_role_id=None,
            admin_role_id=None,
        )
        return await self.repository.create(obj)
