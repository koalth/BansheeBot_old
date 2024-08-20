from src.db import ICharacterRepository
from src.injector import inject
from typing import Optional
from src.entities import Character
from src.raiderIO import RaiderIOClient
from src.mapper import character_response_to_entity
from sqlalchemy.exc import NoResultFound


class CharacterService:

    repository: ICharacterRepository = inject.attr(ICharacterRepository)

    async def add_character(self, character: Character) -> Optional[Character]:
        return await self.repository.add(character)

    async def add_character_to_guild(
        self,
        name: str,
        realm: str,
        region: str,
        discord_user_id: int,
        discord_guild_id: int,
    ) -> Optional[Character]:
        character_io = await RaiderIOClient.getCharacterProfile(name, realm, region)

        if character_io is None:
            raise Exception("charcter_io was None")

        char_entity = character_response_to_entity(character_io)
        char_entity.discord_user_id = discord_user_id
        char_entity.guild_id = discord_guild_id

        char_db = await self.repository.add(char_entity)

        return char_db

    async def get_by_discord_user_id(self, discord_user_id: int) -> Optional[Character]:
        return await self.repository.get_by_discord_user_id(discord_user_id)

    async def get_by_name_and_realm(self, name: str, realm: str) -> Optional[Character]:
        return await self.repository.get_by_name_and_realm(name, realm)

    async def does_character_already_exist(self, name: str, realm: str) -> bool:
        try:
            return (await self.get_by_name_and_realm(name, realm)) is not None
        except NoResultFound:
            return False
