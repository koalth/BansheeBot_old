import os
from typing import Optional
import discord
from discord.ext import commands
from loguru import logger
from src.config import Config
from src.context import Context


class BansheeBot(commands.Bot):

    config: Optional[Config] = None

    def __init__(self) -> None:
        logger.debug("BansheeBot started initialization...")
        super().__init__(
            intents=discord.Intents(
                guilds=True,
                messages=True,
                guild_messages=True,
                message_content=True,
                members=True,
            ),
            activity=discord.Activity(
                type=discord.ActivityType.watching, name="for slash commands!"
            ),
        )
        logger.debug("...BansheeBot ended initialization")

    async def get_application_context(
        self, interaction: discord.Interaction
    ) -> Context:
        return Context(self, interaction)

    def set_config(self, config: Config) -> None:
        logger.debug(f"BansheeBot configured as {os.getenv('BOT_ENV', 'dev')}")
        self.config = config

    def run(self):

        if self.config is None:
            raise Exception("Configuration is not set. Cannot run bot.")

        logger.debug("Loading cogs...")
        cogs_list = [
            "src.cogs.admin_cog",
            "src.cogs.character_cog",
            "src.cogs.setting_cog",
            "src.cogs.guild_cog",
            "src.cogs.raid_cog",
            "src.cogs.general_cog",
        ]
        for cog in cogs_list:
            logger.debug(f"Loading {cog}...")
            self.load_extension(cog)
        logger.debug("...Cogs loaded")
        logger.debug("Bot should be good to go!")
        super().run(self.config.DISCORD_TOKEN)
