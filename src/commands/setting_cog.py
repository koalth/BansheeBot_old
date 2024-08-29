from loguru import logger
import discord
from discord.commands import SlashCommandGroup
from discord.ext import commands
from src.bot import BansheeBot
from src.services import ISettingsService
import inject


class Setting(commands.Cog):

    settingService: ISettingsService = inject.attr(ISettingsService)

    def __init__(self, bot: BansheeBot) -> None:
        self.bot = bot

    @commands.Cog.listener()
    async def on_guild_join(self, guild: discord.Guild):

        if self.settingService.does_guild_settings_exist(str(guild.id)):
            return

        await self.settingService.setup_guild_settings(str(guild.id))

    async def cog_command_error(
        self, ctx: discord.ApplicationContext, error: Exception
    ) -> None:
        logger.error(f"There was a problem in Setting cog: {error}")
        await ctx.respond("Something went wrong :(")
        return await super().cog_command_error(ctx, error)


def setup(bot: BansheeBot) -> None:
    bot.add_cog(Setting(bot))
    logger.debug("Setting cog has loaded successfully")
