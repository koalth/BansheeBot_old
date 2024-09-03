from loguru import logger
import discord
from discord.commands import SlashCommandGroup
from discord.ext import commands
from src.bot import BansheeBot
from src.views import admin_views
from src.services import GuildService, CharacterService
import inject


class Admin(commands.Cog):

    guildService: GuildService = inject.attr(GuildService)
    characterService: CharacterService = inject.attr(CharacterService)

    def __init__(self, bot: BansheeBot) -> None:
        self.bot = bot

    admin = SlashCommandGroup(name="admin", description="Admin commands")

    @admin.command(name="setguild", description="Set the guild for the server")
    async def set_guild(
        self,
        ctx: discord.ApplicationContext,
        name: str,
        realm: str = "Dalaran",
        region: str = "us",
    ):
        guild = await self.guildService.create_guild(
            name, realm, region, str(ctx.guild_id)
        )

        if guild is None:
            return await ctx.respond("There was a problem adding the guild")

        return await ctx.respond(f"`{name}`-`{realm}` has been added")

    @admin.command(name="roster", description="Get the characters on the raid roster")
    async def get_roster(self, ctx: discord.ApplicationContext):

        guild = await self.guildService.get_by_discord_guild_id(str(ctx.guild_id))

        if guild is None:
            return await ctx.respond("There was a problem getting the guild")

        raiders = await self.characterService.get_characters_on_raid_role(guild.id)

        embed = admin_views.AdminRaidRosterEmbed()
        embed.add_characters(raiders)

        return await ctx.respond(embed=embed)

    @admin.command(
        name="test",
        description="This is a test command to make sure the bot is working",
    )
    async def test(self, ctx: discord.ApplicationContext):
        return await ctx.respond("You are smelly!")

    async def cog_command_error(
        self, ctx: discord.ApplicationContext, error: Exception
    ) -> None:
        logger.error(f"There was a problem: {error}")
        await ctx.respond("Something weng wrong :(")
        return await super().cog_command_error(ctx, error)


def setup(bot: BansheeBot) -> None:
    bot.add_cog(Admin(bot))
    logger.debug("Admin cog has loaded successfully")
