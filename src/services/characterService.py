from src.injector import inject
from typing import Optional
from src.entities import Character
from src.raiderIO import RaiderIOClient
from src.mapper import character_response_to_entity


class CharacterService:

    raiderIOClient: RaiderIOClient = inject.attr(RaiderIOClient)

    async def get_character(self, name: str, realm: str, region: str) -> Character:
        raise NotImplementedError()
