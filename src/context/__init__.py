import discord
from discord import ApplicationContext
from src.services import ICharacterService, IGuildService, ISettingService
import inject
from typing import Optional, List


class Context(ApplicationContext):

    _characterService: ICharacterService = inject.attr(ICharacterService)
    _guildService: IGuildService = inject.attr(IGuildService)
    _settingService: ISettingService = inject.attr(ISettingService)

    def get_guild_id(self) -> str:
        ctx_guild = self.guild
        if ctx_guild is None:
            raise ValueError("No guild")
        return str(ctx_guild.id)

    def get_guild_role(self, role_id: str) -> discord.Role:
        assert self.guild
        role = self.guild.get_role(int(role_id))

        if role is None:
            raise ValueError("role not found")
        return role
