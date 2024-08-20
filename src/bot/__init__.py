from typing import Optional
import discord
from discord.ext import commands
from src.config import Config
from loguru import logger


class BansheeBot(commands.Bot):
    config: Config

    def __init__(self) -> None:
        logger.info("BansheeBot started initialization...")
        self.config = Config()
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
        logger.info("...BansheeBot ended initialization")

    # async def start(self, token: str, *, reconnect: bool = True) -> None:
    #     await self.db.start_engine()
    #     return await super().start(token, reconnect=reconnect)

    # async def close(self) -> None:
    #     await self.db.stop_engine()
    #     return await super().close()

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
