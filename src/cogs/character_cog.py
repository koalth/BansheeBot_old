from loguru import logger
import discord
from discord.commands import SlashCommandGroup
from discord.ext import commands
import inject
from src.bot import BansheeBot
from src.services import ICharacterService
from src.views import get_character_embed


class Character(commands.Cog):

    characterGroup: SlashCommandGroup = SlashCommandGroup(
        name="character",
        description="Commands related to a World of Warcraft character",
    )

    characterService: ICharacterService = inject.attr(ICharacterService)

    def __init__(self, bot: BansheeBot) -> None:
        self.bot = bot

    async def cog_command_error(
        self, ctx: discord.ApplicationContext, error: Exception
    ) -> None:
        logger.error(f"There was a problem in Character cog: {error}")
        await ctx.respond("Something went wrong :(")
        return await super().cog_command_error(ctx, error)


def setup(bot: BansheeBot) -> None:
    bot.add_cog(Character(bot))
    logger.debug("Character cog has loaded successfully")
