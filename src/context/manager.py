from contextvars import ContextVar
from functools import wraps
from contextlib import contextmanager
from discord.ext.commands import Context
from typing import Optional
from .custom import BansheeBotCommandContext

discord_context = ContextVar[Optional[BansheeBotCommandContext]](
    "discord_context", default=None
)


@contextmanager
def discord_context_manager(ctx: BansheeBotCommandContext):
    token = discord_context.set(ctx)
    try:
        yield
    finally:
        discord_context.reset(token)


def with_discord_context(func):
    @wraps(func)
    async def wrapper(self, ctx: BansheeBotCommandContext, *args, **kwargs):
        with discord_context_manager(ctx):
            return await func(self, ctx, *args, **kwargs)

    return wrapper


def get_current_context() -> BansheeBotCommandContext:
    ctx = discord_context.get()
    if ctx is None:
        raise ValueError("No discord context available")
    return ctx
