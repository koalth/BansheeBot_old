import discord
from discord.ext import commands


class BansheeBotCommandContext(commands.Context):

    def get_guild(self) -> discord.Guild:
        ctx_guild = self.guild()
        if ctx_guild is None:
            raise ValueError("Guild does not exist")
        return ctx_guild

    def get_guild_id(self) -> str:
        guild = self.get_guild()
        return str(guild.id)
