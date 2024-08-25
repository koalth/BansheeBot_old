import discord
from discord.embeds import Embed
import discord.ui
from src.entities import Character


def get_character_embed(author_name: str, character: Character) -> Embed:

    embed = discord.Embed(
        title=f"{author_name}'s Character", colour=discord.colour.Colour.blurple()
    )

    embed.set_footer(text="Data from Raider.io")
    embed.set_thumbnail(url=character.thumbnail_url)

    embed.add_field(name="Name", value=character.name)
    embed.add_field(name="Item Level", value=str(character.item_level))
    embed.add_field(
        name="Class/Spec", value=f"{character.class_name}/{character.spec_name}"
    )

    return embed
