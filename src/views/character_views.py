import discord
from discord.embeds import Embed
import discord.ui


class LinkCharacterView(discord.ui.View):
    @discord.ui.button(label="Link Character", style=discord.ButtonStyle.primary)
    async def button_callback(
        self, button: discord.ui.Button, interaction: discord.Interaction
    ):
        await interaction.response.send_message("You smell", ephemeral=True)


# class CharacterViews:

#     # linkCharacterEmbed: LinkCharacterEmbed = LinkCharacterEmbed()
#     linkCharacterView: LinkCharacterView = LinkCharacterView()
