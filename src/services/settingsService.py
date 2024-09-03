from typing import Optional, List, Tuple
from src.db import SettingsRepository
from src.entities import Settings
from abc import ABC, abstractmethod, ABCMeta


class ISettingsService(metaclass=ABCMeta):

    @abstractmethod
    async def get_settings(self, discord_guild_id: str) -> Optional[Settings]:
        raise NotImplementedError()

    @abstractmethod
    async def does_guild_settings_exist(self, discord_guild_id: str) -> bool:
        raise NotImplementedError()

    @abstractmethod
    async def setup_guild_settings(self, discord_guild_id: str) -> Optional[Settings]:
        raise NotImplementedError()

    @abstractmethod
    async def update_setting(
        self, discord_guild_id: str, setting_attr: str, attr_value
    ) -> Optional[Settings]:
        raise NotImplementedError()

    @abstractmethod
    async def get_raider_role_id(self, discord_guild_id: str) -> Optional[str]:
        raise NotImplementedError()

    @abstractmethod
    async def get_default_region_and_realm(
        self, discord_guild_id: str
    ) -> Optional[Tuple[str, str]]:
        raise NotImplementedError()


class SettingsService(ISettingsService):

    async def get_settings(self, discord_guild_id: str) -> Optional[Settings]:
        return await SettingsRepository.get_by_discord_guild_id(discord_guild_id)

    async def does_guild_settings_exist(self, discord_guild_id: str) -> bool:
        return (await self.get_settings(discord_guild_id)) is not None

    async def setup_guild_settings(self, discord_guild_id: str) -> Optional[Settings]:
        return await SettingsRepository.add_setting(discord_guild_id)

    async def update_setting(
        self, discord_guild_id: str, setting_attr: str, attr_value
    ) -> Settings | None:
        return await SettingsRepository.update_setting(
            discord_guild_id, setting_attr, attr_value
        )


class MockSettingsService(ISettingsService):

    repo: List[Settings]

    def __init__(self, repo: List[Settings] = []):
        self.repo = repo

    async def get_settings(self, discord_guild_id: str) -> Settings | None:
        result = None
        for item in self.repo:
            if item.discord_guild_id == discord_guild_id:
                result = item
                break
        return result
