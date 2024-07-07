import discord
from discord.commands import SlashCommandGroup
from discord.ext import commands


class DropdownView(discord.ui.View):
    @discord.ui.role_select(placeholder="Select roles...", min_values=1, max_values=20)
    async def role_select_dropdown(
        self, select: discord.ui.Select, interaction: discord.Interaction
    ) -> None:
        await interaction.response.send_message(
            f"You selected the following roles:"
            + f", ".join(f"{role.mention}" for role in select.values)
        )


class Admin(commands.Cog):

    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    admin = SlashCommandGroup(name="admin", description="Admin commands")

    @admin.command(name="set_role", description="Set the role you would like to track")
    async def set_role(self, ctx: discord.ApplicationContext):
        view = DropdownView()
        await ctx.respond("Select roles: ", view=view)


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Admin(bot))
    print("Admin cog has loaded successfully")
