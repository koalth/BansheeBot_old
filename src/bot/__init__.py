import os
from typing import Optional
import discord
from discord.ext import commands
from loguru import logger
from src.config import Config


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

    def set_config(self, config: Config) -> None:
        logger.debug(f"BansheeBot configured as {os.getenv('BOT_ENV', 'dev')}")
        self.config = config

    def run(self):

        if self.config is None:
            raise Exception("Configuration is not set. Cannot run bot.")

        logger.debug("Loading cogs...")
        cogs_list = ["src.commands.admin_cog", "src.commands.character_cog"]
        for cog in cogs_list:
            logger.debug(f"Loading {cog}...")
            self.load_extension(cog)
        logger.debug("...Cogs loaded")
        logger.debug("Bot should be good to go!")
        super().run(self.config.DISCORD_TOKEN)

    async def on_guild_join(self, guild: discord.Guild):
        try:
            if guild.owner is None:
                print("Guild owner was none, cannot create setup dm")
                return
            dm_channel = await guild.owner.create_dm()
            await dm_channel.send(f"Hello! You've added BansheeBot to {guild.name}")
        except Exception as err:
            print("There was a problem when joining guild: ", err)
