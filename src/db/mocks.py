from .interfaces import IGuildRepository, ICharacterRepository
from src.entities import Guild, Character
from typing import List, Optional


class MockGuildRepository(IGuildRepository):

    db: List[Guild]

    def __init__(self):
        self.db = []

    async def get_by_discord_guild_id(self, discord_guild_id: int) -> Optional[Guild]:
        for guild in self.db:
            if guild.discord_guild_id == discord_guild_id:
                return guild
        return None

    async def get_by_guild_name_and_realm(self, name: str, realm: str) -> Guild | None:
        result = None
        for guild in self.db:
            if guild.name == name and guild.realm == realm:
                result = guild

        return result

    async def add(self, entity: Guild) -> Optional[Guild]:
        self.db.append(entity)
        return entity


class MockCharacterRepository(ICharacterRepository):

    db: List[Character]

    def __init__(self):
        self.db = []

    async def get_by_discord_user_id(self, discord_user_id: int) -> Character | None:
        result = None
        for char in self.db:
            if char.discord_user_id == discord_user_id:
                result = char
        return result

    async def get_by_name_and_realm(self, name: str, realm: str) -> Character | None:
        result = None
        for char in self.db:
            if char.name == name and char.realm == realm:
                result = char

        return result

    async def add(self, entity: Character) -> Character | None:
        self.db.append(entity)
        return entity
