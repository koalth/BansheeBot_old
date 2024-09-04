from loguru import logger
import discord
from discord.commands import SlashCommandGroup
from discord.ext import commands
from src.bot import BansheeBot
from src.views import admin
from src.services import IGuildService, ICharacterService, ISettingService
import inject


class Raid(commands.Cog):

    settingService: ISettingService = inject.attr(ISettingService)
    guildService: IGuildService = inject.attr(IGuildService)
    characterService: ICharacterService = inject.attr(ICharacterService)

    raidCommands = SlashCommandGroup(name="raid", description="Raid Roster commands")
    item_levelCommands = raidCommands.create_subgroup(
        name="item_level", description="Item level commands"
    )
    unlinkedCommands = raidCommands.create_subgroup(
        name="unlinked", description="Commands related to unlinked raid members"
    )
    linkedCommands = raidCommands.create_subgroup(
        name="linked", description="Commands relating to linked raid members"
    )

    def __init__(self, bot: BansheeBot) -> None:
        self.bot = bot

    @raidCommands.command(name="show", description="Show the current raid roster")
    async def show_raid(self, ctx: discord.ApplicationContext):
        pass

    @item_levelCommands.command(
        name="set", description="Set the item level requirement for the raid roster"
    )
    async def set_item_level(self, ctx: discord.ApplicationContext, item_level: int):
        pass

    @item_levelCommands.command(
        name="show", description="show the item level requirement for the raid roster"
    )
    async def show_item_level(self, ctx: discord.ApplicationContext):
        pass

    @unlinkedCommands.command(
        name="list", description="List the unlinked members with raid roles"
    )
    async def list_unlinked(self, ctx: discord.ApplicationContext):
        pass

    @unlinkedCommands.command(
        name="message",
        description="Message the unlinked members with raid roles to link their characters",
    )
    async def message_unlinked(self, ctx: discord.ApplicationContext):
        pass

    @linkedCommands.command(
        name="list", description="List the linked members with raid roles"
    )
    async def list_linked(self, ctx: discord.ApplicationContext):
        pass

    @linkedCommands.command(
        name="message",
        description="Message the linked members with raid roles",
    )
    async def message_linked(self, ctx: discord.ApplicationContext):
        pass


def setup(bot: BansheeBot) -> None:
    bot.add_cog(Raid(bot))
    logger.debug("Raid cog has loaded successfully")
