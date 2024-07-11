import discord
from discord.embeds import Embed
from src.models import GuildDTO, CharacterDTO

from typing import List


footer = "Data from Raider.IO"


class GuildViews:

    def getGuildSummary(guild: GuildDTO, characters: List[CharacterDTO]) -> Embed:
        title = f"{guild.wow_guild_name} Summary"
        embed = discord.Embed(
            title=title,
            description="Shows a summary of all the characters registered in the guild\n",
        )
        embed.set_author(name="BansheeBot")

        for character in characters:
            field_value = f"> Item Lv: {character.item_level}"
            embed.add_field(name=character.wow_character_name, value=field_value)

        embed.set_footer(text=footer)

        return embed
