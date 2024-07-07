import discord
from discord.embeds import Embed
from src.raiderIO.models.character import Guild

footer = "Data from Raider.IO"


class GuildViews:

    def getGuildSummary(guild: Guild) -> Embed:
        title = guild.name.capitalize() + "'s Summary"
        embed = discord.Embed(title=title, description="")
        embed.set_author(name="BansheeBot")

        embed.set_footer(text=footer)

        return embed
