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

    # @discord.slash_command(
    #     name="character",
    #     description="Gets a quick summary of a World of Warcraft character",
    # )
    # async def character_get(
    #     self, ctx: discord.ApplicationContext, name: str, realm: str, region: str = "us"
    # ):
    #     pass

    # @characterGroup.command(
    #     name="get",
    #     description="Retrieves a quick summary of a World of Warcraft Character from RaiderIO",
    # )
    # async def get(
    #     self,
    #     ctx: discord.ApplicationContext,
    #     name: str,
    #     realm: str = "Dalaran",
    #     region: str = "us",
    # ):
    #     character = await self.characterService.get_character_from_raider_io(
    #         name, realm, region
    #     )

    #     if character is None:
    #         return await ctx.respond(
    #             "I wasn't able to grab your character. Please try again."
    #         )

    #     return await ctx.respond(
    #         embed=get_character_embed(ctx.author.display_name, character)
    #     )

    async def cog_command_error(
        self, ctx: discord.ApplicationContext, error: Exception
    ) -> None:
        logger.error(f"There was a problem in Character cog: {error}")
        await ctx.respond("Something went wrong :(")
        return await super().cog_command_error(ctx, error)


def setup(bot: BansheeBot) -> None:
    bot.add_cog(Character(bot))
    logger.debug("Character cog has loaded successfully")
