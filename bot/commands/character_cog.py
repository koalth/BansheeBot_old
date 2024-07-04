from typing import Optional

import discord
from discord.commands import SlashCommandGroup
from discord.ext import commands

from bot.raiderIO import get_character
from bot.views.character_views import display_character_summary


class Character(commands.Cog):

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        print("Character cog is initializing...")

    character = SlashCommandGroup(name="character")

    @character.command(name="get_char")
    async def get_char(self, ctx, name: str, realm: Optional[str] = "Dalaran"):
        try:
            discord_user_id = ctx.author.id
            character_io = await get_character(name, realm)

            if character_io is None:
                await ctx.respond(f"Character {name}-{realm} does not exist")
                return

            else:
                await ctx.respond(
                    f"Item level: {character_io.gear.item_level_equipped}"
                )

        except Exception as exception:
            print(exception)
            await ctx.respond("Something went wrong")

    @character.command(name="get_character_summary")
    async def get_character_summary(
        self, ctx, name: str, realm: Optional[str] = "Dalaran"
    ):
        try:
            character_io = await get_character(name, realm)

            if character_io is None:
                await ctx.respond(f"Character {name}-{realm} does not exist")
                return
            else:
                embed = display_character_summary(character_io)
                await ctx.respond(embed=embed)

        except Exception as exception:
            print(exception)
            await ctx.respond("Something went wrong")


def setup(bot):
    bot.add_cog(Character(bot))
    print("Character cog has loaded successfully")
