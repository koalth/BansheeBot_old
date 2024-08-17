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
        )

        embed.set_author(name="BansheeBot")

        for character in guild.characters:
            field_value = f"> Item Lv: {character.item_level}"
            embed.add_field(name=character.name, value=field_value)

        embed.set_footer(text=footer)

        return embed
