import discord
from discord.ext import commands


def get_guild(ctx: commands.Context) -> discord.Guild:
    ctx_guild = ctx.guild()
    if ctx_guild is None:
        raise ValueError("Guild was none")
    return ctx_guild
