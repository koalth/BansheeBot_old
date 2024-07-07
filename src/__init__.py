import discord
from discord.ext import commands
from src.db import BansheeBotDB
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
ch.setFormatter(formatter)
logger.addHandler(ch)


class BansheeBot(commands.Bot):

    db: BansheeBotDB

    def __init__(self) -> None:
        logger.debug("BansheeBot started initialization...")
        self.db = BansheeBotDB()
        super().__init__(
            intents=discord.Intents(
                guilds=True, messages=True, guild_messages=True, message_content=True
            ),
            activity=discord.Activity(
                type=discord.ActivityType.watching, name="for slash commands!"
            ),
        )
        logger.debug("...BansheeBot ended initialization")

    async def start(self, token: str, *, reconnect: bool = True) -> None:
        await self.db.start_engine()
        return await super().start(token, reconnect=reconnect)

    async def close(self) -> None:
        await self.db.stop_engine()
        return await super().close()

    def run(self, token: str):
        cogs_list = ["src.commands.character_cog", "src.commands.admin_cog"]
        for cog in cogs_list:
            self.load_extension(cog)
        super().run(token)

    async def on_guild_join(self, guild: discord.Guild):
        try:
            await self.db.addDiscordGuild(guild.id, guild.name)
        except Exception as err:
            print("Could not add discord guild: ", err)
