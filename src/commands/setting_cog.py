from loguru import logger
import discord
from discord.commands import SlashCommandGroup
from discord.ext import commands
from src.bot import BansheeBot
from src.services import ISettingsService
from src.views import settings_view
import inject


class Setting(commands.Cog):

    settingCommands = SlashCommandGroup(
        name="settings", description="Commands related to the server's settings"
    )

    settingService: ISettingsService = inject.attr(ISettingsService)

    def __init__(self, bot: BansheeBot) -> None:
        self.bot = bot

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
            return ctx.respond("Setting doesn't exist.")

        return await ctx.respond(
            "Please select a region to set as default",
            view=settings_view.SettingsSelectRegion(guild_id, timeout=30),
            ephemeral=True,
        )

    async def cog_command_error(
        self, ctx: discord.ApplicationContext, error: Exception
    ) -> None:
        logger.error(f"There was a problem in Setting cog: {error}")
        await ctx.respond("Something went wrong :(")
        return await super().cog_command_error(ctx, error)


def setup(bot: BansheeBot) -> None:
    bot.add_cog(Setting(bot))
    logger.debug("Setting cog has loaded successfully")
