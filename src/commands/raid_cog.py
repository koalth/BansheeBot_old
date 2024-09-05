from loguru import logger
import discord
from discord.commands import SlashCommandGroup
from discord.ext import commands
from src.bot import BansheeBot
from src.views import raid
from src.entities import GuildUpdate
from src.services import IGuildService, ICharacterService, ISettingService
import inject
from typing import List


class Raid(commands.Cog):

    bot: BansheeBot

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

    def _get_guild_id(self, ctx: discord.ApplicationContext) -> str:
        assert ctx.guild
        return str(ctx.guild.id)

    async def _get_unlinked_members(
        self, ctx: discord.ApplicationContext
    ) -> List[discord.Member]:
        assert type(ctx.guild) is discord.Guild
        ctx.guild.name
        guild_id = self._get_guild_id(ctx)
        if not (
            await self.settingService.does_guild_settings_exist(
                discord_guild_id=guild_id
            )
        ):
            raise ValueError("Settings do not exist")

        settings = await self.settingService.get_by_discord_guild_id(
            discord_guild_id=guild_id
        )

        if settings.raider_role_id is None:
            raise ValueError("Raider role not found")

        guild = await self.guildService.get_by_discord_guild_id(guild_id)
        if guild is None:
            raise ValueError("Guild not found")

        ctx_guild = ctx.guild
        assert type(ctx_guild) is discord.Guild

        raider_role = ctx_guild.get_role(int(settings.raider_role_id))
        assert type(raider_role) == discord.Role

        members = []
        for member in raider_role.members:
            if not await self.characterService.has_character(str(member.id)):
                members.append(member)

        return members

    async def _get_linked_members(
        self, ctx: discord.ApplicationContext
    ) -> List[discord.Member]:
        assert type(ctx.guild) is discord.Guild
        ctx.guild.name
        guild_id = self._get_guild_id(ctx)
        if not (
            await self.settingService.does_guild_settings_exist(
                discord_guild_id=guild_id
            )
        ):
            raise ValueError("Settings do not exist")

        settings = await self.settingService.get_by_discord_guild_id(
            discord_guild_id=guild_id
        )

        if settings.raider_role_id is None:
            raise ValueError("Raider role not found")

        guild = await self.guildService.get_by_discord_guild_id(guild_id)
        if guild is None:
            raise ValueError("Guild not found")

        ctx_guild = ctx.guild
        assert type(ctx_guild) is discord.Guild

        raider_role = ctx_guild.get_role(int(settings.raider_role_id))
        assert type(raider_role) == discord.Role

        members = []
        for member in raider_role.members:
            if await self.characterService.has_character(str(member.id)):
                members.append(member)

        return members

    @raidCommands.command(name="show", description="Show the current raid roster")
    async def show(self, ctx: discord.ApplicationContext):
        guild_id = str(ctx.guild_id)
        guild = await self.guildService.get_by_discord_guild_id(guild_id)

        raiders = await self.characterService.get_characters_with_raid_role(guild.id)

        embed = raid.RaidRosterShowEmbed()
        embed.add_characters(raiders, guild.item_level_requirement)

        return await ctx.respond(embed=embed)

    @item_levelCommands.command(
        name="set", description="Set the item level requirement for the raid roster"
    )
    async def set_item_level(self, ctx: discord.ApplicationContext, item_level: int):
        guild_id = str(ctx.guild_id)
        guild = await self.guildService.get_by_discord_guild_id(
            discord_guild_id=guild_id
        )

        guild_update = GuildUpdate(item_level_requirement=item_level)

        updated_guild = await self.guildService.update(guild.id, guild_update)

        return await ctx.respond(
            f"Item level Requirement set to `{updated_guild.item_level_requirement}`"
        )

    @item_levelCommands.command(
        name="show", description="show the item level requirement for the raid roster"
    )
    async def show_item_level(self, ctx: discord.ApplicationContext):
        guild_id = str(ctx.guild_id)
        guild = await self.guildService.get_by_discord_guild_id(
            discord_guild_id=guild_id
        )

        if guild.item_level_requirement is None:
            return await ctx.respond(f"There is currently no item level requirement")

        return await ctx.respond(
            f"Item level Requirement is currently set to `{guild.item_level_requirement}`"
        )

    @unlinkedCommands.command(
        name="list", description="List the unlinked members with raid roles"
    )
    async def list_unlinked(self, ctx: discord.ApplicationContext):
        ctx_guild = ctx.guild
        assert type(ctx_guild) is discord.Guild

        embed = discord.Embed(
            title="Unlinked Raiders",
            description="These are members with the set raider role but have not linked their character",
            colour=0x0060FF,
        )

        members = await self._get_unlinked_members(ctx)
        member_names = []
        for member in members:
            if not await self.characterService.has_character(str(member.id)):
                member_names.append(member.display_name)

        embed.add_field(name="Name", value="\n".join(member_names))

        return await ctx.respond(embed=embed)

    @unlinkedCommands.command(
        name="message",
        description="Message the unlinked members with raid roles to link their characters",
    )
    async def message_unlinked(self, ctx: discord.ApplicationContext):
        assert type(ctx.guild) is discord.Guild
        guild_id = self._get_guild_id(ctx)
        ctx_guild = ctx.guild
        assert type(ctx_guild) is discord.Guild

        guild = await self.guildService.get_by_discord_guild_id(
            discord_guild_id=guild_id
        )

        embed = discord.Embed(
            title="Link Character",
            description=f"Please link your World of Warcraft character to be tracked for `{ctx.guild.name}`",
            color=discord.Color.orange(),
        )

        members = await self._get_unlinked_members(ctx)

        for member in members:
            if not await self.characterService.has_character(str(member.id)):
                await member.send(
                    embed=embed,
                    view=raid.RaidRosterMemberLinkCharacterView(
                        discord_guild_id=guild_id, guild_id=guild.id
                    ),
                )

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
