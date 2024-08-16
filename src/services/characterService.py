from src.views import GuildViewModel, CharacterViewModel
from src.db import CharacterRepository
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

    async def get_by_discord_user_id(self, discord_user_id: int) -> CharacterViewModel:
        character_result = await self.repository.get_by_discord_id(discord_user_id)

        return CharacterViewModel(
            name=character_result.name,
            region=character_result.region,
            realm=character_result.realm,
            item_level=character_result.item_level,
            char_class=character_result.class_name,
            profile_url=character_result.profile_url,
            thumbnail_url=character_result.thumbnail_url,
        )

    async def get_by_name_and_realm(self, name: str, realm: str) -> CharacterViewModel:
        character_result = await self.repository.get_by_name_and_realm(name, realm)

        return CharacterViewModel(
            name=character_result.name,
            region=character_result.region,
            realm=character_result.realm,
            item_level=character_result.item_level,
            char_class=character_result.class_name,
            profile_url=character_result.profile_url,
            thumbnail_url=character_result.thumbnail_url,
        )

    async def does_character_already_exist(self, name: str, realm: str) -> bool:
        try:
            return (await self.get_by_name_and_realm(name, realm)) is not None
        except NoResultFound:
            return False
