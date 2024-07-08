from typing import Optional
import discord
from discord.commands import SlashCommandGroup
from discord.ext import commands

from src import BansheeBot

from src.views.admin_views import AdminRoleSelectView
from src.views.guild_views import GuildViews

from src.raiderIO.client import RaiderIOClient


class Admin(commands.Cog):

    def __init__(self, bot: BansheeBot) -> None:
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

    @admin.command(
        name="set_wow_guild",
        description="Set this servers World of Warcraft guild",
    )
    @discord.ext.commands.has_permissions(administrator=True)
    async def set_wow_guild(
        self,
        ctx: discord.ApplicationContext,
        name: str,
        realm: Optional[str] = "Dalaran",
    ):
        try:
            guild_io = await RaiderIOClient.getGuildProfile(name, realm)

            if guild_io is None:
                await ctx.respond(f"Guild {name}-{realm} was not found.")
            else:
                # embed = GuildViews.getGuildSummary(guild_io)
                # await ctx.respond(embed=embed)

                # add new guild to database and link it to current server
                await self.bot.db.addWowGuildToDiscordGuild(
                    ctx.guild_id, guild_io.name, guild_io.region, guild_io.realm
                )
                await ctx.respond(f"Guild {name}-{realm} was added.")

        except Exception as err:
            print(err)
            await ctx.respond("Something went wrong")


def setup(bot: commands.Bot) -> None:
    bot.add_cog(Admin(bot))
    print("Admin cog has loaded successfully")
