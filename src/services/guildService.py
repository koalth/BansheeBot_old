from src.views.viewmodels import GuildViewModel
from src.db import GuildRepository
from src.raiderIO import RaiderIOClient


class GuildService:

    repository: GuildRepository

    def __init__(self):
        self.repository = GuildRepository()

    async def set_wow_guild(
        self, name: str, realm: str, region: str, discord_guild_id: int
    ) -> GuildViewModel:

        guild_result = await self.repository.get_by_discord_guild_id(discord_guild_id)

        if guild_result is not None:
            return GuildViewModel(
                name=guild_result.name,
                region=guild_result.region,
                realm=guild_result.realm,
            )

        guild_io = await RaiderIOClient.getGuildProfile(name, realm, region)

        if guild_io is None:
            raise Exception("guild io was None")

        guild_db = await self.repository.create_guild(
            name, realm, region, discord_guild_id
        )

        return GuildViewModel(
            name=guild_db.name, region=guild_db.region, realm=guild_db.realm
        )