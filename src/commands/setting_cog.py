from loguru import logger
import discord
from discord.commands import SlashCommandGroup
from discord.ext import commands
from src.bot import BansheeBot
from src.services import ISettingsService
import inject


class Setting(commands.Cog):

    settingCommands = SlashCommandGroup = SlashCommandGroup(
        name="settings", description="Commands related to the server's settings"
    )

    settingService: ISettingsService = inject.attr(ISettingsService)

    def __init__(self, bot: BansheeBot) -> None:
        self.bot = bot

    @commands.Cog.listener()
    async def on_guild_join(self, guild: discord.Guild):

        guild_id = str(guild.id)

        if self.settingService.does_guild_settings_exist(guild_id):
            return

        await self.settingService.setup_guild_settings(guild_id)
        return

    @settingCommands.command()
    async def set_default_region(self, ctx: discord.ApplicationContext):
        pass
