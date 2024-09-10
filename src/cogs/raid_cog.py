from loguru import logger
import discord
from discord.commands import SlashCommandGroup
from discord.ext import commands, tasks
from discord import guild_only

from .base import Cog
from src.context import Context
from src.bot import BansheeBot
from src.views import raid
from src.entities import GuildUpdate

from typing import List


class Raid(Cog):

    raidCommands = SlashCommandGroup(
        name="raid",
        description="Raid Roster commands",
    )
    item_levelCommands = raidCommands.create_subgroup(
        name="item_level", description="Item level commands"
    )
    unlinkedCommands = raidCommands.create_subgroup(
        name="unlinked",
        description="Commands related to unlinked raid members",
    )
    linkedCommands = raidCommands.create_subgroup(
        name="linked",
        description="Commands relating to linked raid members",
    )

    def _get_guild_id(self, ctx: Context) -> str:
        assert ctx.guild
        return str(ctx.guild.id)

    async def _get_unlinked_members(self, ctx: Context) -> List[discord.Member]:
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
            if not (await self.characterService.has_character(str(member.id))):
                members.append(member)

        return members

    async def _get_linked_members(self, ctx: Context) -> List[discord.Member]:
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
    async def show(self, ctx: Context):
        guild_id = str(ctx.guild_id)
        guild = await self.guildService.get_by_discord_guild_id(guild_id)

        raiders = await self.characterService.get_characters_with_raid_role(guild.id)

        embed = raid.RaidRosterShowEmbed()
        embed.add_characters(raiders, guild.item_level_requirement)

        return await ctx.respond(embed=embed)

    @item_levelCommands.command(
        name="set", description="Set the item level requirement for the raid roster"
    )
    @guild_only()
    async def set_item_level(self, ctx: Context, item_level: int):
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
    @guild_only()
    async def show_item_level(self, ctx: Context):
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
    async def list_unlinked(self, ctx: Context):
        ctx_guild = ctx.guild
        assert type(ctx_guild) is discord.Guild

        embed = discord.Embed(
            title="Unlinked Raiders",
            description="These are members with the set raider role but have not linked their character",
            colour=discord.Colour.dark_orange(),
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
    async def message_unlinked(self, ctx: Context):
        assert type(ctx.guild) is discord.Guild
        ctx_guild = ctx.guild
        assert type(ctx_guild) is discord.Guild

        embed = discord.Embed(
            title="Link Character",
            description=f"Please link your World of Warcraft character to be tracked for **{ctx.guild.name}** using the `/add` command in the server",
            color=discord.Color.orange(),
        )

        members = await self._get_unlinked_members(ctx)

        for member in members:
            await member.send(
                embed=embed,
            )

        return await ctx.respond("Messages has been sent.", ephemeral=True)

    @linkedCommands.command(
        name="list", description="List the linked members with raid roles"
    )
    async def list_linked(self, ctx: Context):
        ctx_guild = ctx.guild
        assert type(ctx_guild) is discord.Guild

        embed = discord.Embed(
            title="Linked Raiders",
            description="These are members with the set raider role but have not linked their character",
            colour=discord.Colour.dark_green(),
        )

        members = await self._get_linked_members(ctx)
        member_names = []
        for member in members:
            member_names.append(member.display_name)

        embed.add_field(name="Name", value="\n".join(member_names))

        return await ctx.respond(embed=embed)

    @linkedCommands.command(
        name="message",
        description="Message the linked members with raid roles",
    )
    async def message_linked(self, ctx: Context, message: str):
        assert type(ctx.guild) is discord.Guild
        ctx_guild = ctx.guild
        assert type(ctx_guild) is discord.Guild

        members = await self._get_linked_members(ctx)
        for member in members:
            await member.send(content=f"Message from {ctx.author.name}: {message}")

        return await ctx.respond("Messages has been sent.", ephemeral=True)

    async def cog_command_error(self, ctx: Context, error: Exception) -> None:
        logger.error(f"There was a problem in Raid cog: {error}")
        await ctx.respond("Something went wrong :(")
        return await super().cog_command_error(ctx, error)


def setup(bot: BansheeBot) -> None:
    bot.add_cog(Raid(bot))
    logger.debug("Raid cog has loaded successfully")