import discord

from discord.embeds import Embed

from src.models import CharacterDTO
from src.views.viewmodels import CharacterViewModel

footer = "Data from Raider.IO"


class CharacterViews:

    @staticmethod
    def getCharacterSummary(character: CharacterDTO) -> Embed:
        title = character.name.capitalize() + "'s Summary"
        embed = discord.Embed(title=title, description="", url=character.profile_url)

        embed.set_author(name="BansheeBot")

        embed.add_field(name="Class", value=character.class_name, inline=True)
        # embed.add_field(name="Specialization", value=character., inline=True)
        # embed.add_field(name="Role", value=character., inline=True)

        embed.add_field(
            name="Item Level",
            value=str(character.item_level),
            inline=True,
        )

        embed.set_thumbnail(url=character.thumbnail_url)

        embed.set_footer(text=footer)
        return embed
