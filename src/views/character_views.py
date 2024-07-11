import discord

from discord.embeds import Embed

from src.models import CharacterDTO

footer = "Data from Raider.IO"


class CharacterViews:

    def getCharacterSummary(
        character: CharacterDTO, bot_user: discord.User = None
    ) -> Embed:
        title = character.name.capitalize() + "'s Summary"
        embed = discord.Embed(title=title, description="", url=character.profile_url)

        embed.set_author(name="BansheeBot")

        embed.add_field(name="Class", value=character.class_name, inline=True)
        embed.add_field(name="Specialization", value=character.spec_name, inline=True)
        embed.add_field(name="Role", value=character.role.value, inline=True)
        embed.add_field(
            name="Item Level", value=character.gear.item_level_equipped, inline=True
        )

        embed.set_thumbnail(url=character.thumbnail_url)

        embed.set_footer(text=footer)
        return embed
