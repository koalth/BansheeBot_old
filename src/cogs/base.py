from discord.ext import commands
from src.bot import BansheeBot


class Cog(commands.Cog):

    def __init__(self, bot: BansheeBot) -> None:
        self.bot = bot
