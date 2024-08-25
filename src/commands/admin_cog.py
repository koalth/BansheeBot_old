from loguru import logger
import discord
from discord.commands import SlashCommandGroup
from discord.ext import commands
from src.bot import BansheeBot
from src.services import CharacterService
from typing import Optional
from src.injector import inject
from src.views.character_views import LinkCharacterView


class Admin(commands.Cog):

    characterService: CharacterService = inject.attr(CharacterService)

    def __init__(self, bot: BansheeBot) -> None:
        self.bot = bot

    admin = SlashCommandGroup(name="admin", description="Admin commands")

    @admin.command(
        name="test",
        description="This is a test command to make sure the bot is working",
    )
    async def test(self, ctx: discord.ApplicationContext):
        return await ctx.respond("You are smelly!")

    async def cog_command_error(
        self, ctx: discord.ApplicationContext, error: Exception
    ) -> None:
        logger.error(f"There was a problem: {error}")
        await ctx.respond("Something weng wrong :(")
        return await super().cog_command_error(ctx, error)


def setup(bot: BansheeBot) -> None:
    bot.add_cog(Admin(bot))
    logger.debug("Admin cog has loaded successfully")
