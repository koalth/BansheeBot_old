from loguru import logger
import discord
from discord.commands import SlashCommandGroup
from discord.ext import commands
from src.bot import BansheeBot
from src.services import ISettingService, IGuildService
from src.entities import SettingUpdate
from src.views import setting
import inject
from typing import Optional


class Setting(commands.Cog):

    settingService: ISettingService = inject.attr(ISettingService)
    guildService: IGuildService = inject.attr(IGuildService)

    def __init__(self, bot: BansheeBot) -> None:
        self.bot = bot

    settingCommands = SlashCommandGroup(
        name="settings", description="Commands related to the server's settings"
    )
    admin_role = settingCommands.create_subgroup(name="admin_role")
    raider_role = settingCommands.create_subgroup(name="raider_role")
    region = settingCommands.create_subgroup(name="region")
    realm = settingCommands.create_subgroup(name="realm")

    async def _get_guild_role(
        self, role_id: Optional[str], ctx: discord.Interaction
    ) -> Optional[discord.Role]:
        if ctx.guild is None:
            raise Exception("guild not on context")

        if role_id is None:
            return None

        role = ctx.guild.get_role(int(role_id))

        if role is None:
            raise Exception("role not found")
        return role

    @settingCommands.command(
        name="show", description="Show the current server settings."
    )
    async def show(self, ctx: discord.ApplicationContext):
        guild_id = str(ctx.guild_id)
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
    async def admin_role_set(self, ctx: discord.ApplicationContext):
        pass

    @raider_role.command(
        name="set",
        description="Set the raider role. This role will be used for the raid roster",
    )
    async def raider_role_set(self, ctx: discord.ApplicationContext):
        pass

    @region.command(
        name="set",
        description="Set the default region. This region will be used for all requests",
    )
    async def region_set(self, ctx: discord.ApplicationContext):
        pass

    @realm.command(
        name="set",
        description="Set the default realm. This realm will be used for all requests",
    )
    async def realm_set(self, ctx: discord.ApplicationContext):
        pass

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

    @settingCommands.command(
        name="init",
        description="Initalizes the settings for the server if not already initialized.",
    )
    async def init_settings(self, ctx: discord.ApplicationContext):
        guild_id = str(ctx.guild_id)
        logger.debug(f"guild id: {guild_id}")
        if await self.settingService.does_guild_settings_exist(
            discord_guild_id=guild_id
        ):
            return await ctx.respond("Setting already exist")

        await self.settingService.setup_guild_settings(discord_guild_id=guild_id)

        return await ctx.respond("Guild setting have been created")

    @settingCommands.command(name="region")
    async def set_default_region(self, ctx: discord.ApplicationContext):
        guild_id = str(ctx.guild_id)
        if not (
            await self.settingService.does_guild_settings_exist(
                discord_guild_id=guild_id
            )
        ):
            return await ctx.respond("Setting doesn't exist.")

        return await ctx.respond(
            "Please select a region to set as default",
            view=setting.SettingsSelectRegion(guild_id, timeout=30),
            ephemeral=True,
        )

    @settingCommands.command(name="realm")
    async def set_default_realm(self, ctx: discord.ApplicationContext, realm: str):
        guild_id = str(ctx.guild_id)
        if not (
            await self.settingService.does_guild_settings_exist(
                discord_guild_id=guild_id
            )
        ):
            return await ctx.respond("Setting doesn't exist.")

        settings = await self.settingService.get_by_discord_guild_id(
            discord_guild_id=guild_id
        )

        update_obj = SettingUpdate(default_realm=realm)

        updated_settings = await self.settingService.update(settings.id, update_obj)

        return await ctx.respond(
            f"Default realm has been set to {updated_settings.default_realm}",
            ephemeral=True,
        )

    @settingCommands.command(name="raiderrole", description="Set the raider role")
    async def set_raider_role(self, ctx: discord.ApplicationContext):
        guild_id = str(ctx.guild_id)
        if not (
            await self.settingService.does_guild_settings_exist(
                discord_guild_id=guild_id
            )
        ):
            return await ctx.respond("Setting doesn't exist.")

        return await ctx.respond(
            "Please select a role for your raiders",
            view=setting.SettingsRaiderRoleSelect(
                discord_guild_id=guild_id, timeout=30
            ),
            ephemeral=True,
        )

    @settingCommands.command(
        name="sendraidlinks",
        description="Send all raiders a dm to add their wow character",
    )
    async def send_raider_links(self, ctx: discord.ApplicationContext):
        guild_id = str(ctx.guild_id)
        if not (
            await self.settingService.does_guild_settings_exist(
                discord_guild_id=guild_id
            )
        ):
            return await ctx.respond("Setting doesn't exist.")

        settings = await self.settingService.get_by_discord_guild_id(
            discord_guild_id=guild_id
        )

        if settings.raider_role_id is None:
            return await ctx.respond("Raider role doesn't exist.")

        ctx_guild = ctx.interaction.guild
        if ctx_guild is None:
            return await ctx.respond("Guild doesn't exist.")

        raider_role = ctx_guild.get_role(int(settings.raider_role_id))

        if raider_role is None:
            return await ctx.respond("Role wasn't found")

        guild = await self.guildService.get_by_discord_guild_id(guild_id)
        if guild is None:
            return await ctx.respond("guild wasn't found")

        if guild.id is None:
            return await ctx.respond("guild id wasn't found")

        for member in raider_role.members:
            await member.send(
                content="Hello! Please add your wow character using the button below!",
                view=setting.SettingsRaiderRoleMemberSelectView(
                    discord_guild_id=guild_id, guild_id=guild.id
                ),
            )

        return await ctx.respond("Members have been sent a message", ephemeral=True)

    async def cog_command_error(
        self, ctx: discord.ApplicationContext, error: Exception
    ) -> None:
        logger.error(f"There was a problem in Setting cog: {error}")
        await ctx.respond("Something went wrong :(")
        return await super().cog_command_error(ctx, error)


def setup(bot: BansheeBot) -> None:
    bot.add_cog(Setting(bot))
    logger.debug("Setting cog has loaded successfully")
