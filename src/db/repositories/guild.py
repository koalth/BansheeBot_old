from .base import GenericRepository
from .interfaces import IGuildRepository
from ..models.guild import GuildOrm
from src.entities import Guild, GuildCreate, GuildUpdate


class GuildRepository(
    GenericRepository[GuildOrm, GuildCreate, GuildUpdate, Guild], IGuildRepository
):
    def __init__(self):
        super().__init__(GuildOrm, Guild)
