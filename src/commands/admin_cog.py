from loguru import logger
import discord
from discord.commands import SlashCommandGroup
from discord.ext import commands
from src.bot import BansheeBot
from src.views import admin
from src.services import IGuildService, ICharacterService
from src.entities import GuildCreate
import inject


class Admin(commands.Cog):

    guildService: IGuildService = inject.attr(IGuildService)
    characterService: ICharacterService = inject.attr(ICharacterService)

    def __init__(self, bot: BansheeBot) -> None:
        self.bot = bot

    @discord.command(name="balls")
    async def balls(self, ctx: discord.ApplicationContext):
        return await ctx.respond("balls")

    async def cog_command_error(
        self, ctx: discord.ApplicationContext, error: Exception
    ) -> None:
        logger.error(f"There was a problem: {error}")
        await ctx.respond("Something weng wrong :(")
        return await super().cog_command_error(ctx, error)


def setup(bot: BansheeBot) -> None:
    bot.add_cog(Admin(bot))
    logger.debug("Admin cog has loaded successfully")
