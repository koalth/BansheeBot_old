from src.views import GuildViewModel
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
