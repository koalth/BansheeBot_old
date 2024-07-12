import discord


class AdminRoleSelectView(discord.ui.View):
    @discord.ui.role_select(placeholder="Select roles...", min_values=1, max_values=20)
    async def role_select_dropdown(
        self, select: discord.ui.Select, interaction: discord.Interaction
    ) -> None:
        await interaction.response.send_message(
            f"You selected the following roles:"
            + f", ".join(f"{role}" for role in select.values)
        )
