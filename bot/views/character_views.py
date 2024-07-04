import discord


from bot.raiderIO.models.character import Character

footer = "Data from Raider.IO"


def display_character_summary(character: Character, bot_user: discord.User = None):
    title = character.name.capitalize() + "'s Summary"
    embed = discord.Embed(
        title=title,
        description="",
    )

    embed.set_author(name="BansheeBot")

    embed.add_field(name="Class", value=character.c_class, inline=True)
    # embed.add_field(name="Last Spec", value=charac)
    # embed.set_thumbnail(ch)

    embed.set_footer(text=footer)
    return embed
