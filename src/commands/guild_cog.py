from loguru import logger
import discord
from discord.commands import SlashCommandGroup
from discord.ext import commands
from src.bot import BansheeBot
from src.services import IGuildService
from src.entities import GuildCreate
import inject
from enum import Enum


class Region(Enum):
    US = "us"
    EU = "eu"


class Guild(commands.Cog):

    guildService: IGuildService = inject.attr(IGuildService)

    def __init__(self, bot: BansheeBot) -> None:
        self.bot = bot

    guildCommands = SlashCommandGroup(
        name="guild", description="Commands for the guild"
    )

    @guildCommands.command(name="show", description="Show a summary of the WoW Guild")
    async def show_guild(self, ctx: discord.ApplicationContext):
        guild_id = str(ctx.guild_id)
        guild = await self.guildService.get_by_discord_guild_id(guild_id)

        embed = discord.Embed(
            title=f"{guild.name}",
            description="Shows a summary of the guild tied to the server",
        )

        embed.add_field(name="Realm", value=guild.realm)
        embed.add_field(name="Region", value=guild.region)

        return await ctx.respond(embed=embed)

    @guildCommands.command(name="set", description="Set the server's Wow guild")
    async def set_guild(
        self, ctx: discord.ApplicationContext, name: str, realm: str, region: str
    ):
        guild_id = str(ctx.guild_id)
        guild = await self.guildService.create(
            GuildCreate(
                name=name,
                realm=realm,
                region=region,
                discord_guild_id=guild_id,
                item_level_requirement=None,
            )
        )

        return await ctx.respond(f"`{guild.name}`-`{guild.realm}` has been added")


def setup(bot: BansheeBot) -> None:
    bot.add_cog(Guild(bot))
    logger.debug("Guild cog has loaded successfully")
