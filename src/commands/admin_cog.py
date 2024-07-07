import discord
from discord.commands import SlashCommandGroup
from discord.ext import commands

from src.views.admin_views import AdminRoleSelectView


class Admin(commands.Cog):

    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    admin = SlashCommandGroup(name="admin", description="Admin commands")

    @admin.command(name="set_role", description="Set the role you would like to track")
    @discord.ext.commands.has_permissions(administrator=True)
    async def set_role(self, ctx: discord.ApplicationContext):
        view = AdminRoleSelectView()
        await ctx.respond("Select roles: ", view=view, ephemeral=True)

    @admin.command(
        name="delete_last_messages",
        description="Delete the last n messages in the current channel",
    )
    @discord.ext.commands.has_permissions(administrator=True)
    async def delete_last_messages(
        self, ctx: discord.ApplicationContext, amount: int
    ) -> None:
        messages = await ctx.channel.history(limit=amount).flatten()
        for msg in messages:
            await msg.delete()

        await ctx.send("Deleted messages")


def setup(bot: commands.Bot) -> None:
    bot.add_cog(Admin(bot))
    print("Admin cog has loaded successfully")
