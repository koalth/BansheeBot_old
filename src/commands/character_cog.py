from typing import Optional, List

import discord
from discord.commands import SlashCommandGroup
from discord.ext import commands

import logging

logger = logging.getLogger(__name__)
logger.setLevel(level=logging.DEBUG)
ch = logging.StreamHandler()
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
ch.setFormatter(formatter)
logger.addHandler(ch)

from src.raiderIO import RaiderIOClient
from src.views.viewmodels import CharacterViewModel


class Character(commands.Cog):

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        logger.info("Character cog is initializing...")

    character = SlashCommandGroup(name="character")

    # @character.command(name="get_char")
    # async def get_char(
    #     self,
    #     ctx: discord.ApplicationContext,
    #     name: str,
    #     realm: str = "Dalaran",
    #     region: str = "us",
    # ):
    #     character_io = await RaiderIOClient.getCharacterProfile(name, realm, region)

    #     if character_io is None or character_io.item_level is None:
    #         await ctx.respond(f"Character {name}-{realm} does not exist")
    #         return

    #     else:

    #         await ctx.respond(f"Item level: {character_io.item_level}")

    # @character.command(name="get_character_summary")
    # async def get_character_summary(
    #     self,
    #     ctx: discord.ApplicationContext,
    #     name: str,
    #     realm: str = "Dalaran",
    #     region: str = "us",
    # ):
    #     character_io = await RaiderIOClient.getCharacterProfile(name, realm, region)
    #     if character_io is None:
    #         await ctx.respond(f"Character {name}-{realm} does not exist")
    #         return
    #     else:

    #         embed = CharacterViews.getCharacterSummary(character_io)
    #         await ctx.respond(embed=embed)

    async def cog_command_error(
        self, ctx: discord.ApplicationContext, error: Exception
    ) -> None:
        logger.error(f"There was a problem: {error}")
        await ctx.respond("Something weng wrong :(")
        return await super().cog_command_error(ctx, error)


def setup(bot: commands.Bot):
    bot.add_cog(Character(bot))
    logger.info("Character cog has loaded successfully")
