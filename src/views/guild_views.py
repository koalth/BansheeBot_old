import discord
from discord.embeds import Embed
from src.models import GuildDTO, CharacterDTO

from typing import List


footer = "Data from Raider.IO"


class GuildViews:

    @staticmethod
    def getGuildSummary(guild: GuildDTO, characters: List[CharacterDTO]) -> Embed:
        title = f"{guild.name} Summary"
        embed = discord.Embed(
            title=title,
            description="Shows a summary of all the characters registered in the guild\n",
        )
        embed.set_author(name="BansheeBot")

        for character in characters:
            if character.gear is not None:
                field_value = f"> Item Lv: {character.gear.item_level_equipped}"
                embed.add_field(name=character.name, value=field_value)

        embed.set_footer(text=footer)

        return embed
