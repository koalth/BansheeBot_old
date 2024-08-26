from loguru import logger
from src.injector import inject
from typing import Optional
from src.entities import Character
from src.raiderIO import IRaiderIOClient
from src.mapper import character_response_to_entity


class CharacterService:

    raiderIOClient: IRaiderIOClient = inject.attr(IRaiderIOClient)

    async def get_character(
        self, name: str, realm: str, region: str
    ) -> Optional[Character]:

        try:
            character = await self.raiderIOClient.getCharacterProfile(
                name, realm, region
            )

            if character == None:
                return None

            return character_response_to_entity(character)
        except Exception:
            logger.exception("There was problem in CharacterService")
            raise
