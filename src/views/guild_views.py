import discord
from discord.embeds import Embed
from src.entities import Character, Guild

from typing import List


footer = "Data from Raider.IO"


class GuildViews:

    @staticmethod
    def getGuildSummary(guild: Guild) -> Embed:
        title = f"{guild.name} Summary"
        embed = discord.Embed(
            title=title,
            description="Shows a summary of all the characters registered in the guild\n",
            color=discord.Colour.blurple(),
        )

        embed.set_author(name="BansheeBot")

        names = "\n".join([character.name for character in guild.characters])
        item_levels = "\n".join(
            [str(character.item_level) for character in guild.characters]
        )

        embed.add_field(name="Members", value=names, inline=True)
        embed.add_field(name="Item Level", value=item_levels, inline=True)

        embed.set_footer(text=footer)

        return embed
