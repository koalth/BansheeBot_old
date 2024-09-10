from loguru import logger
import discord
from discord.commands import SlashCommandGroup
from discord.ext import commands
from discord import guild_only

from .base import Cog
from src.bot import BansheeBot
from src.services import ISettingService, IGuildService
from src.entities import SettingUpdate
from src.views import setting

import inject
from typing import Optional
from enum import Enum


class Region(Enum):
    US = "us"
    EU = "eu"


class Setting(Cog):

    bot: BansheeBot

    settingService: ISettingService = inject.attr(ISettingService)
    guildService: IGuildService = inject.attr(IGuildService)

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

    def __init__(self, bot: BansheeBot) -> None:
        self.bot = bot

    async def _get_guild_role(
        self, role_id: Optional[str], ctx: discord.Interaction
    ) -> Optional[discord.Role]:
        if ctx.guild is None:
            raise Exception("guild not on context")

        if role_id is None:
            return None

        role = ctx.guild.get_role(int(role_id))

        if role is None:
            raise ValueError("role not found")
        return role

    @settingCommands.command(
        name="show", description="Show the current server settings."
    )
    @commands.is_owner()
    @guild_only()
    async def show(self, ctx: discord.ApplicationContext):
        assert ctx.guild()

        guild_id = str(ctx.guild())
        settings = await self.settingService.get_by_discord_guild_id(guild_id)

        admin_role = await self._get_guild_role(
            settings.admin_role_id,
            ctx.interaction,
        )

        raider_role = await self._get_guild_role(
            settings.raider_role_id,
            ctx.interaction,
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
    async def set_admin_role(self, ctx: discord.ApplicationContext, role: discord.Role):
        guild_id = str(ctx.guild_id)
        if not (
            await self.settingService.does_guild_settings_exist(
                discord_guild_id=guild_id
            )
        ):
            return await ctx.respond("Settings must exist first before you can do this")

        settings = await self.settingService.get_by_discord_guild_id(
            discord_guild_id=guild_id
        )

        update_obj = SettingUpdate(admin_role_id=str(role.id))

        newly_updated = await self.settingService.update(settings.id, update_obj)

        return await ctx.respond(
            f"You have set {role.mention} as the Admin role", ephemeral=True
        )

    @raider_role.command(
        name="set",
        description="Set the raider role. This role will be used for the raid roster",
    )
    @commands.is_owner()
    @guild_only()
    async def set_raider_role(
        self, ctx: discord.ApplicationContext, role: discord.Role
    ):
        guild_id = str(ctx.guild_id)
        if not (
            await self.settingService.does_guild_settings_exist(
                discord_guild_id=guild_id
            )
        ):
            return await ctx.respond("Settings must exist first before you can do this")

        settings = await self.settingService.get_by_discord_guild_id(
            discord_guild_id=guild_id
        )

        update_obj = SettingUpdate(raider_role_id=str(role.id))

        newly_updated = await self.settingService.update(settings.id, update_obj)

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
    async def set_default_region(self, ctx: discord.ApplicationContext, region: Region):
        guild_id = str(ctx.guild_id)
        if not (
            await self.settingService.does_guild_settings_exist(
                discord_guild_id=guild_id
            )
        ):
            return await ctx.respond("Settings must exist first before you can do this")

        settings = await self.settingService.get_by_discord_guild_id(guild_id)

        update_obj = SettingUpdate(default_region=region.value)

        await self.settingService.update(settings.id, update_obj)

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
    async def set_default_realm(self, ctx: discord.ApplicationContext, realm: str):
        guild_id = str(ctx.guild_id)
        if not (
            await self.settingService.does_guild_settings_exist(
                discord_guild_id=guild_id
            )
        ):
            return await ctx.respond("Settings must exist first before you can do this")

        settings = await self.settingService.get_by_discord_guild_id(
            discord_guild_id=guild_id
        )

        update_obj = SettingUpdate(default_realm=realm)

        newly_updated = await self.settingService.update(settings.id, update_obj)

        return await ctx.respond(
            f"You have set `{newly_updated.default_realm}`", ephemeral=True
        )

    @settingCommands.command(
        name="init",
        description="Initalizes the settings for the server if not already initialized.",
    )
    @commands.is_owner()
    @guild_only()
    async def init_settings(self, ctx: discord.ApplicationContext):
        guild_id = str(ctx.guild_id)
        if await self.settingService.does_guild_settings_exist(
            discord_guild_id=guild_id
        ):
            return await ctx.respond("Setting already exist")

        await self.settingService.setup_guild_settings(discord_guild_id=guild_id)

        return await ctx.respond("Guild setting have been created")

    @commands.Cog.listener()
    async def on_guild_join(self, guild: discord.Guild):

        guild_id = str(guild.id)
        logger.debug(f"guild_id: {guild_id}")

        if await self.settingService.does_guild_settings_exist(
            discord_guild_id=guild_id
        ):
            return

        await self.settingService.setup_guild_settings(guild_id)
        return

    async def cog_command_error(
        self, ctx: discord.ApplicationContext, error: Exception
    ) -> None:
        logger.error(f"There was a problem in Setting cog: {error}")
        await ctx.respond("Something went wrong :(")
        return await super().cog_command_error(ctx, error)


def setup(bot: BansheeBot) -> None:
    bot.add_cog(Setting(bot))
    logger.debug("Setting cog has loaded successfully")
