import discord
from discord.commands import SlashCommandGroup
from discord.ext import commands

from loguru import logger

from src.context import Context
from .base import Cog
from src.bot import BansheeBot


class Admin(Cog):

    def __init__(self, bot: BansheeBot) -> None:
        self.bot = bot

    @discord.slash_command()
    async def balls(self, ctx: Context):
        guild_id = ctx.get_guild_id()
        settings = await ctx._settingService.get_by_discord_guild_id(guild_id)

        return await ctx.respond(settings.default_realm)

    async def cog_command_error(self, ctx: Context, error: Exception) -> None:
        logger.error(f"There was a problem: {error}")
        await ctx.respond("Something weng wrong :(")
        return await super().cog_command_error(ctx, error)


def setup(bot: BansheeBot) -> None:
    bot.add_cog(Admin(bot))
    logger.debug("Admin cog has loaded successfully")
