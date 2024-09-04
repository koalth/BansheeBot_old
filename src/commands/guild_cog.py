from loguru import logger
import discord
from discord.commands import SlashCommandGroup
from discord.ext import commands
from src.bot import BansheeBot
from src.services import IGuildService
import inject


class Guild(commands.Cog):

    guildService: IGuildService = inject.attr(IGuildService)

    def __init__(self, bot: BansheeBot) -> None:
        self.bot = bot

    guildCommands = SlashCommandGroup(
        name="guild", description="Commands for the guild"
    )

    @guildCommands.command(name="show", description="Show a summary of the WoW Guild")
    async def show_guild(self, ctx: discord.ApplicationContext):
        pass

    @guildCommands.command(name="set", description="Set the server's Wow guild")
    async def set_guild(self, ctx: discord.ApplicationContext, name: str):
        pass


def setup(bot: BansheeBot) -> None:
    bot.add_cog(Guild(bot))
    logger.debug("Guild cog has loaded successfully")
