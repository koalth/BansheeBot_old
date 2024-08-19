from typing import List, Optional
from abc import ABC, abstractmethod

from src.injector import inject
from src.entities import Character


class ICharacterRepository(ABC):

    @abstractmethod
    async def get_by_discord_user_id(self, discord_user_id: int) -> Optional[Character]:
        raise NotImplementedError()

    @abstractmethod
    async def get_by_name_and_realm(self, name: str, realm: str) -> Optional[Character]:
        raise NotImplementedError()

    @abstractmethod
    async def add(self, entity: Character) -> Optional[Character]:
        raise NotImplementedError()
