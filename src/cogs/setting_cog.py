from loguru import logger
import discord
from discord.commands import SlashCommandGroup
from discord.ext import commands
from discord import guild_only

from .base import Cog
from src.context import Context
from src.bot import BansheeBot
from src.entities import SettingUpdate
from src.views import setting

from enum import Enum
from functools import wraps


def ensure_settings_exist():
    def decorator(func):
        @wraps(func)
        async def wrapper(self, ctx: Context, *args, **kwargs):
            if not (await ctx.check_settings_exist()):
                return await ctx.respond("Settings must exist")
            return await func(self, ctx, *args, **kwargs)

        return wrapper

    return decorator


class Region(Enum):
    US = "us"
    EU = "eu"


class Setting(Cog):

    settingCommands = SlashCommandGroup(
        name="settings",
        description="Commands related to the server's settings",
    )
    admin_role = settingCommands.create_subgroup(
        name="admin_role",
    )
    raider_role = settingCommands.create_subgroup(
        name="raider_role",
    )
    region = settingCommands.create_subgroup(
        name="region",
    )
    realm = settingCommands.create_subgroup(
        name="realm",
    )

    @settingCommands.command(
        name="show", description="Show the current server settings."
    )
    @commands.is_owner()
    @guild_only()
    @ensure_settings_exist()
    async def show(self, ctx: Context):

        guild_id = ctx.get_guild_id()
        settings = await ctx._settingService.get_by_discord_guild_id(guild_id)

        admin_role = None
        if settings.admin_role_id is not None:
            admin_role = ctx.get_guild_role(settings.admin_role_id)

        if settings.raider_role_id is not None:
            raider_role = ctx.get_guild_role(
                settings.raider_role_id,
            )

        return await ctx.respond(
            embed=setting.SettingsShowEmbed(
                region=settings.default_region,
                realm=settings.default_realm,
                admin_role=admin_role.name if admin_role is not None else None,
                raider_role=raider_role.name if raider_role is not None else None,
            )
        )

    @admin_role.command(
        name="set", description="Set the admin role. Admins can use admin commands"
    )
    @commands.is_owner()
    @guild_only()
    @ensure_settings_exist()
    async def set_admin_role(self, ctx: Context, role: discord.Role):
        guild_id = ctx.get_guild_id()
        settings = await ctx._settingService.get_by_discord_guild_id(
            discord_guild_id=guild_id
        )

        update_obj = SettingUpdate(admin_role_id=str(role.id))
        await ctx._settingService.update(settings.id, update_obj)

        return await ctx.respond(
            f"You have set {role.mention} as the Admin role", ephemeral=True
        )

    @raider_role.command(
        name="set",
        description="Set the raider role. This role will be used for the raid roster",
    )
    @commands.is_owner()
    @guild_only()
    @ensure_settings_exist()
    async def set_raider_role(self, ctx: Context, role: discord.Role):

        guild_id = ctx.get_guild_id()
        settings = await ctx._settingService.get_by_discord_guild_id(
            discord_guild_id=guild_id
        )

        update_obj = SettingUpdate(raider_role_id=str(role.id))
        await ctx._settingService.update(settings.id, update_obj)

        return await ctx.respond(
            f"You have set {role.mention} as the Raider role", ephemeral=True
        )

    @region.command(
        name="set",
        description="Set the default region. This region will be used for all requests",
    )
    @discord.option(
        "region", Region, description="Region in which guild resides", default=Region.US
    )
    @commands.is_owner()
    @guild_only()
    @ensure_settings_exist()
    async def set_default_region(self, ctx: Context, region: Region):
        guild_id = ctx.get_guild_id()
        settings = await ctx._settingService.get_by_discord_guild_id(guild_id)

        update_obj = SettingUpdate(default_region=region.value)

        await ctx._settingService.update(settings.id, update_obj)

        return await ctx.respond(
            f"Default region has been set to `{region.name}`",
            ephemeral=True,
        )

    @realm.command(
        name="set",
        description="Set the default realm. This realm will be used for all requests",
    )
    @commands.is_owner()
    @guild_only()
    @ensure_settings_exist()
    async def set_default_realm(self, ctx: Context, realm: str):

        guild_id = ctx.get_guild_id()
        settings = await ctx._settingService.get_by_discord_guild_id(
            discord_guild_id=guild_id
        )

        update_obj = SettingUpdate(default_realm=realm)

        newly_updated = await ctx._settingService.update(settings.id, update_obj)

        return await ctx.respond(
            f"You have set `{newly_updated.default_realm}`", ephemeral=True
        )

    @settingCommands.command(
        name="init",
        description="Initalizes the settings for the server if not already initialized.",
    )
    @commands.is_owner()
    @guild_only()
    async def init_settings(self, ctx: Context):
        guild_id = str(ctx.guild_id)
        if await ctx._settingService.does_guild_settings_exist(
            discord_guild_id=guild_id
        ):
            return await ctx.respond("Setting already exist")

        await ctx._settingService.setup_guild_settings(discord_guild_id=guild_id)

        return await ctx.respond("Guild setting have been created")

    @commands.Cog.listener()
    async def on_guild_join(self, ctx: Context, guild: discord.Guild):

        guild_id = str(guild.id)
        logger.debug(f"guild_id: {guild_id}")

        if await ctx._settingService.does_guild_settings_exist(
            discord_guild_id=guild_id
        ):
            return

        await ctx._settingService.setup_guild_settings(guild_id)
        return

    async def cog_command_error(self, ctx: Context, error: Exception) -> None:
        logger.error(f"There was a problem in Setting cog: {error}")
        await ctx.respond("Something went wrong :(")
        return await super().cog_command_error(ctx, error)


def setup(bot: BansheeBot) -> None:
    bot.add_cog(Setting(bot))
    logger.debug("Setting cog has loaded successfully")
