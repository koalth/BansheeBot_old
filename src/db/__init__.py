from typing import Optional
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession

from src.config import Config

from src.models import GuildDTO, CharacterDTO, Region
from src.db.repositories import GuildRepository, CharacterRepository

import logging

logger = logging.getLogger("Database")
logger.setLevel(level=logging.DEBUG)
ch = logging.StreamHandler()
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
ch.setFormatter(formatter)
logger.addHandler(ch)


class BansheeBotDB:

    guildRepository: GuildRepository
    characterRepository: CharacterRepository

    def __init__(self, config: Config):
        self.guildRepository = GuildRepository()
        self.characterRepository = CharacterRepository()
        self.config = config
        self.engine = create_async_engine(self.config.SQLITE_URL)

    async def start_engine(self):
        logger.info("DB engine started...")

    async def stop_engine(self):
        await self.engine.dispose()
        logger.info("...DB engine disposed")

    async def createWowGuild(
        self, name: str, realm: str = "Dalaran", region: Region = Region.US
    ) -> Optional[GuildDTO]:
        async with AsyncSession(self.engine) as session:
            return await self.guildRepository.add(session, name, realm, region)

    async def getWowGuildByDiscordGuildId(
        self, discord_guild_id: int
    ) -> Optional[GuildDTO]:
        async with AsyncSession(self.engine) as session:
            return await self.guildRepository.get_by_discord_guild_id(
                session, discord_guild_id
            )

    async def getWowGuildById(self, id: int) -> Optional[GuildDTO]:
        async with AsyncSession(self.engine) as session:
            return await self.guildRepository.get_by_id(session, id)

    async def createWowCharacter(
        self, wow_character: CharacterDTO
    ) -> Optional[CharacterDTO]:
        async with AsyncSession(self.engine) as session:
            return await self.characterRepository.add(session, wow_character)
