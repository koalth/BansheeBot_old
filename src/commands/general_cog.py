from loguru import logger
import discord
from discord.ext import commands
import inject
from src.bot import BansheeBot
from src.services import ICharacterService, ISettingService, IGuildService


class General(commands.Cog):

    characterService: ICharacterService = inject.attr(ICharacterService)
    settingService: ISettingService = inject.attr(ISettingService)
    guildService: IGuildService = inject.attr(IGuildService)

    def __init__(self, bot: BansheeBot) -> None:
        self.bot = bot

    @discord.slash_command(
        name="add",
        description="Add your World of Warcraft character to be tracked and viewed by your guild",
    )
    async def add_character(self, ctx: commands.Context, name: str, realm: str):
        pass

    @discord.slash_command(
        name="get",
        description="Get your World of Warcraft character currently associated in the discord guild",
    )
    async def get_character(self, ctx: commands.Context):
        pass

    async def cog_command_error(
        self, ctx: discord.ApplicationContext, error: Exception
    ) -> None:
        logger.error(f"There was a problem in General cog: {error}")
        await ctx.respond("Something went wrong :(")
        return await super().cog_command_error(ctx, error)


def setup(bot: BansheeBot) -> None:
    bot.add_cog(General(bot))
    logger.debug("General cog has loaded successfully")
