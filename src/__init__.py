import discord
from discord.ext import commands

from src.db import BansheeBotDB


class BansheeBot(commands.Bot):

    db: BansheeBotDB

    def __init__(self) -> None:
        self.db = BansheeBotDB()
        super().__init__(
            intents=discord.Intents(guilds=True),
            activity=discord.Activity(
                type=discord.ActivityType.watching, name="for slash commands!"
            ),
        )

    async def start(self, token: str, *, reconnect: bool = True) -> None:
        await self.db.start_engine()
        return await super().start(token, reconnect=reconnect)

    async def close(self) -> None:
        await self.db.stop_engine()
        return await super().close()

    def run(self, token: str):
        cogs_list = ["src.commands.character_cog"]
        for cog in cogs_list:
            self.load_extension(cog)
        super().run(token)

    async def on_guild_join(self, guild: discord.Guild):
        try:
            await self.db.addDiscordGuild(guild.id, guild.name)
        except Exception as err:
            print("Could not add discord guild: ", err)
