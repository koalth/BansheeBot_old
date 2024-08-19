import logging
import discord
from discord.commands import SlashCommandGroup
from discord.ext import commands
from src import BansheeBot
from src.views import GuildViews
from src.services import GuildService, CharacterService


logger = logging.getLogger(__name__)
logger.setLevel(level=logging.DEBUG)
ch = logging.StreamHandler()
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
ch.setFormatter(formatter)
logger.addHandler(ch)


class Admin(commands.Cog):

    guildService: GuildService
    characterService: CharacterService

    def __init__(self, bot: BansheeBot) -> None:
        self.bot = bot

        self.guildService = GuildService()
        self.characterService = CharacterService()

    admin = SlashCommandGroup(name="admin", description="Admin commands")

    # @admin.command(name="set_role", description="Set the role you would like to track")
    # @commands.has_permissions(administrator=True)
    # async def set_role(self, ctx: discord.ApplicationContext):
    #     view = AdminRoleSelectView()
    #     await ctx.respond("Select roles: ", view=view, ephemeral=True)

    @admin.command(
        name="set_wow_guild",
        description="Set this servers World of Warcraft guild",
    )
    @commands.has_permissions(administrator=True)
    async def set_wow_guild(
        self,
        ctx: discord.ApplicationContext,
        name: str,
        realm: str = "Dalaran",
        region: str = "us",
    ):

        # discord is already tied to a wow guild
        guildExist = await self.guildService.is_discord_already_linked(ctx.guild_id)
        if guildExist:
            await ctx.respond(f"`{ctx.guild.name} is already tied to a wow guild`")
            return

        # wow_guild is already tied to discord
        wowGuildAlreadyLinked = await self.guildService.is_wow_guild_already_linked(
            name, realm
        )
        if wowGuildAlreadyLinked:
            await ctx.respond(f"`{name}-{realm} is already tied to a discord server`")
            return

        # wow guild cannot be found
        # TODO add something

        # everything good

        wow_guild = await self.guildService.add_wow_guild(
            name, realm, region, ctx.guild_id
        )

        if wow_guild is None:
            await ctx.respond(f"`{name}-{realm} was not found.`")
            return

        await ctx.respond(
            f"Guild `{wow_guild.name}-{wow_guild.realm}` was added to `{ctx.guild.name}`"
        )

    @admin.command(
        name="add_character_to_guild",
        description="Adds a wow character to the server's wow guild",
    )
    @commands.has_permissions(administrator=True)
    async def add_character_to_guild(
        self,
        ctx: discord.ApplicationContext,
        member: discord.Member,
        name: str,
        realm: str = "Dalaran",
        region: str = "us",
    ):

        # ensure that wow guild is linked to this server
        wow_guild = await self.guildService.get_by_discord_guild_id(ctx.guild_id)

        if wow_guild is None:
            await ctx.respond(
                "A WoW guild needs to be setup first before adding characters"
            )
            return

        # check if character already exists in guild (discord guild)
        wow_char = await self.characterService.get_by_discord_user_id(member.id)

        if wow_char is not None:
            await ctx.respond(f"`{wow_char.name}` is already registered")
            return

        wow_char = await self.characterService.add_character_to_guild(
            name, realm, region, member.id, ctx.guild_id
        )

        if wow_char is None:
            await ctx.respond("Something went wrong adding character to guild")
            return

        await ctx.respond(f"`{wow_char.name}` was added to `{wow_guild.name}`")

    @admin.command(
        name="get_guild_summary",
        description="Gets a short summary of the guild member's and their item levels",
    )
    @commands.has_permissions(administrator=True)
    async def get_guild_summary(self, ctx: discord.ApplicationContext):

        wow_guild = await self.guildService.get_by_discord_guild_id(ctx.guild_id)

        if wow_guild is None:
            await ctx.respond("No guild was found")
            return

        embed = GuildViews.getGuildSummary(wow_guild)

        await ctx.respond(embed=embed)

    async def cog_command_error(
        self, ctx: discord.ApplicationContext, error: Exception
    ) -> None:
        logger.error(f"There was a problem: {error}")
        await ctx.respond("Something weng wrong :(")
        return await super().cog_command_error(ctx, error)


def setup(bot: BansheeBot) -> None:
    bot.add_cog(Admin(bot))
    logger.info("Admin cog has loaded successfully")
