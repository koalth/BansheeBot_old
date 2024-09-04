from loguru import logger
import discord
from discord.commands import SlashCommandGroup
from discord.ext import commands
from src.bot import BansheeBot
from src.views import admin
from src.services import IGuildService, ICharacterService
from src.entities import GuildCreate
import inject


class Admin(commands.Cog):

    guildService: IGuildService = inject.attr(IGuildService)
    characterService: ICharacterService = inject.attr(ICharacterService)

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

        guild_id = str(ctx.guild_id)
        guild = await self.guildService.create(
            GuildCreate(
                name=name,
                realm=realm,
                region=region,
                discord_guild_id=guild_id,
                item_level_requirement=None,
            )
        )

        return await ctx.respond(f"`{guild.name}`-`{guild.realm}` has been added")

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
