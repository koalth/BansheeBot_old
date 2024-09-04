from src.db import GuildOrm, GenericRepository, IGenericRepository
from src.entities import Guild, GuildCreate, GuildUpdate
from abc import ABCMeta


class IGuildRepository(
    IGenericRepository[GuildOrm, GuildCreate, GuildUpdate, Guild], metaclass=ABCMeta
):
    pass


class GuildRepository(
    IGuildRepository, GenericRepository[GuildOrm, GuildCreate, GuildUpdate, Guild]
):
    def __init__(self):
        super().__init__(GuildOrm, Guild)
