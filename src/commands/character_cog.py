from typing import Optional, List

import discord
from discord.commands import SlashCommandGroup
from discord.ext import commands
from discord import option

import logging

logger = logging.getLogger(__name__)
logger.setLevel(level=logging.DEBUG)
ch = logging.StreamHandler()
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
ch.setFormatter(formatter)
logger.addHandler(ch)


from src.raiderIO.client import RaiderIOClient
from src.views.character_views import CharacterViews


class Character(commands.Cog):

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        logger.info("Character cog is initializing...")

    character = SlashCommandGroup(name="character")

    @character.command(name="get_char")
    async def get_char(
        self,
        ctx: discord.ApplicationContext,
        name: str,
        realm: Optional[str] = "Dalaran",
    ):
        try:
            character_io = await RaiderIOClient.getCharacterProfile(name, realm)

            if character_io is None:
                await ctx.respond(f"Character {name}-{realm} does not exist")
                return

            else:
                await ctx.respond(
                    f"Item level: {character_io.gear.item_level_equipped}"
                )

        except Exception as err:
            logger.error(f"Something went wrong with get_char: {err}")
            await ctx.respond("Something went wrong")

    @character.command(name="get_character_summary")
    async def get_character_summary(
        self,
        ctx: discord.ApplicationContext,
        name: str,
        realm: Optional[str] = "Dalaran",
    ):
        try:
            character_io = await RaiderIOClient.getCharacterProfile(name, realm)
            if character_io is None:
                await ctx.respond(f"Character {name}-{realm} does not exist")
                return
            else:
                embed = CharacterViews.getCharacterSummary(character_io)
                await ctx.respond(embed=embed)

        except Exception as err:
            logger.error(f"Something went wrong with get_character_summary: {err}")
            await ctx.respond("Something went wrong")


def setup(bot: commands.Bot):
    bot.add_cog(Character(bot))
    logger.info("Character cog has loaded successfully")
