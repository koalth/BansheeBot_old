from typing import List, Optional
from src.db import CharacterRepository
from src.entities import Character, Guild
from src.raiderIO import RaiderIOClient
from sqlalchemy.exc import NoResultFound
import logging

logger = logging.getLogger("GuildService")
logger.setLevel(level=logging.DEBUG)
ch = logging.StreamHandler()
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
ch.setFormatter(formatter)
logger.addHandler(ch)


class CharacterService:
    repository: CharacterRepository

    def __init__(self, repository: CharacterRepository = CharacterRepository()):
        self.repository = repository

    async def add_character(self, character: Character) -> Optional[Character]:
        return await self.repository.add(character)

    async def get_by_discord_user_id(self, discord_user_id: int) -> Optional[Character]:
        return await self.repository.get_by_discord_user_id(discord_user_id)

    async def get_by_name_and_realm(self, name: str, realm: str) -> Optional[Character]:
        return await self.repository.get_by_name_and_realm(name, realm)

    async def does_character_already_exist(self, name: str, realm: str) -> bool:
        try:
            return (await self.get_by_name_and_realm(name, realm)) is not None
        except NoResultFound:
            return False
