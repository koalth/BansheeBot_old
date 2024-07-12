import logging
from typing import Optional
import discord
from discord.commands import SlashCommandGroup
from discord.ext import commands

from src.models import GuildDTO

logger = logging.getLogger(__name__)
logger.setLevel(level=logging.DEBUG)
ch = logging.StreamHandler()
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
ch.setFormatter(formatter)
logger.addHandler(ch)


from src import BansheeBot
from src.views.admin_views import AdminRoleSelectView
from src.views.guild_views import GuildViews
from src.raiderIO import RaiderIOClient


class Admin(commands.Cog):

    def __init__(self, bot: BansheeBot) -> None:
        self.bot = bot

    admin = SlashCommandGroup(name="admin", description="Admin commands")

    @admin.command(name="set_role", description="Set the role you would like to track")
    @commands.has_permissions(administrator=True)
    async def set_role(self, ctx: discord.ApplicationContext):
        view = AdminRoleSelectView()
        await ctx.respond("Select roles: ", view=view, ephemeral=True)

    @admin.command(
        name="delete_last_messages",
        description="Delete the last n messages in the current channel",
    )
    @commands.has_permissions(administrator=True)
    async def delete_last_messages(
        self, ctx: discord.ApplicationContext, amount: int
    ) -> None:

        if ctx.channel is None:
            raise Exception("Channel was none")

        messages = await ctx.channel.history(limit=amount).flatten()  # type: ignore
        for msg in messages:
            await msg.delete()

        await ctx.send("Deleted messages")

    @admin.command(
        name="set_wow_guild",
        description="Set this servers World of Warcraft guild",
    )
    @commands.has_permissions(administrator=True)
    async def set_wow_guild(
        self,
        ctx: discord.ApplicationContext,
        name: str,
        realm: str = "Dalaran",
    ):
        try:
            guild_io = await RaiderIOClient.getGuildProfile(name, realm)

            if guild_io is None:
                await ctx.respond(f"Guild {name}-{realm} was not found.")
            else:
                if ctx.guild is None:
                    raise Exception("Guild was none")
                # add new guild to database and link it to current server
                wow_guild = await self.bot.db.addWowGuild(ctx.guild.id, guild_io)

                if wow_guild is None:
                    raise Exception

                await ctx.respond(f"Guild {name}-{realm} was added to {ctx.guild.name}")

        except Exception as err:
            logger.error(f"There was a problem with set_wow_guild: {err}")
            await ctx.respond("Something went wrong")

    @admin.command(
        name="add_character_to_guild",
        description="Adds a WoW character to the server's WoW guild",
    )
    @commands.has_permissions(administrator=True)
    async def add_character_to_guild(
        self,
        ctx: discord.ApplicationContext,
        name: str,
        realm: str = "Dalaran",
    ):
        try:
            character_io = await RaiderIOClient.getCharacterProfile(name, realm)
            if character_io is None:
                await ctx.respond(
                    f"Character {name}-{realm} was not found or does not exist"
                )
                return
            else:

                if ctx.guild is None:
                    raise Exception("Guild was none")

                wow_character = await self.bot.db.addWowCharacterToWowGuild(
                    ctx.guild.id, character_io, ctx.author.id
                )

                if wow_character is None or wow_character.wow_guild is None:
                    await ctx.respond("There was a problem adding chracter")
                    raise Exception
                else:
                    await ctx.respond(
                        f"{wow_character.name} was added to {wow_character.wow_guild.name}"
                    )

        except Exception as err:
            logger.error(f"There was a problem with add_character_to_guild: {err}")
            await ctx.respond("Something went wrong")

    @admin.command(
        name="get_guild_summary",
        description="Get a summary of the current guild",
    )
    @commands.has_permissions(administrator=True)
    async def get_guild_summary(self, ctx: discord.ApplicationContext):
        try:
            if ctx.guild is None:
                raise Exception("Guild was none")

            wow_guild_db = await self.bot.db.getWowGuild(ctx.guild.id)

            if wow_guild_db is None or len(wow_guild_db.wow_characters) == 0:
                print("Wow guild was none")
                raise Exception

            wow_guild = GuildDTO(**wow_guild_db.model_dump())

            embed = GuildViews.getGuildSummary(wow_guild, wow_guild.characters)

            await ctx.respond(embed=embed)

        except Exception as err:
            logger.error(f"There was a problem with get_guild_summary: {err}")
            await ctx.respond("Something went wrong")


def setup(bot: BansheeBot) -> None:
    bot.add_cog(Admin(bot))
    logger.info("Admin cog has loaded successfully")
