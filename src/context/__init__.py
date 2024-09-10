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
        if not isinstance(self.guild, discord.Guild):
            raise TypeError("Guild not set")

        role = self.guild.get_role(int(role_id))

        if role is None:
            raise ValueError(f"Role with ID {role_id} not found")

        return role

    async def check_settings_exist(self) -> bool:
        guild_id = self.get_guild_id()
        return (
            await self._settingService.does_guild_settings_exist(guild_id) is not None
        )
