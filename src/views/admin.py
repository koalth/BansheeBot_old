import discord
from typing import List
from src.entities import Character


class AdminRoleSelectView(discord.ui.View):
    @discord.ui.role_select(placeholder="Select roles...", min_values=1, max_values=20)
    async def role_select_dropdown(
        self, select: discord.ui.Select, interaction: discord.Interaction
    ) -> None:
        await interaction.response.send_message(
            "You selected the following roles:"
            + ", ".join(f"{role}" for role in select.values)
        )


class AdminRaidRosterEmbed(discord.Embed):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.title = "Raid Roster"
        self.set_footer(text="Data from Raider.IO")

    def add_characters(self, characters: List[Character]):

        names = "\n".join([character.name for character in characters])
        item_levels = "\n".join(
            [f"{str(character.item_level)} ✅" for character in characters]
        )
        class_spec_names = "\n".join(
            [f"{char.class_name}/{char.spec_name}" for char in characters]
        )
        self.add_field(name="Members", value=names, inline=True)
        self.add_field(name="Item Level", value=item_levels, inline=True)
        self.add_field(name="Class/Spec", value=class_spec_names, inline=True)
