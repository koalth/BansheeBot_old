from typing import Optional
import discord
from discord.ext import commands
from src.config import config
from loguru import logger


class BansheeBot(commands.Bot):

    intents: discord.Intents
    activity: discord.Activity

    def __init__(self) -> None:
        logger.debug("BansheeBot started initialization...")
        self.config = config
        super().__init__(intents=self.intents, activity=self.activity)
        logger.debug("...BansheeBot ended initialization")

    def setup(self):
        self.intents = discord.Intents(
            guilds=True,
            messages=True,
            guild_messages=True,
            message_content=True,
            members=True,
        )

        self.activity = discord.Activity(
            type=discord.ActivityType.watching, name="for slash commands!"
        )

    def run(self):
        cogs_list = ["src.commands.admin_cog"]
        for cog in cogs_list:
            self.load_extension(cog)
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
