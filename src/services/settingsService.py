from loguru import logger
from typing import Optional, List
from src.db import add_setting, get_by_discord_guild_id
from src.entities import Settings
from abc import ABC, abstractmethod


class ISettingsService(ABC):

    @abstractmethod
    async def get_settings(self, discord_guild_id: str) -> Optional[Settings]:
        raise NotImplementedError()

    @abstractmethod
    async def does_guild_settings_exist(self, discord_guild_id: str) -> bool:
        raise NotImplementedError()

    @abstractmethod
    async def setup_guild_settings(self, discord_guild_id: str) -> Optional[Settings]:
        raise NotImplementedError()


class SettingsService(ISettingsService):

    async def get_settings(self, discord_guild_id: str) -> Optional[Settings]:
        return await get_by_discord_guild_id(discord_guild_id)

    async def does_guild_settings_exist(self, discord_guild_id: str) -> bool:
        return (await self.get_settings(discord_guild_id)) is not None

    async def setup_guild_settings(self, discord_guild_id: str) -> Optional[Settings]:
        return await add_setting(discord_guild_id)


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
