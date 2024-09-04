from loguru import logger
import inject
from typing import Optional
from src.entities import Guild, GuildCreate, GuildUpdate
from src.external.raiderIO import IRaiderIOClient
from src.db import GuildOrm, IGuildRepository
from .base import GenericService, IGenericService
from abc import abstractmethod, ABCMeta


class IGuildService(
    IGenericService[GuildOrm, GuildCreate, GuildUpdate, Guild], metaclass=ABCMeta
):
    pass


class GuildService(
    IGuildService, GenericService[GuildOrm, GuildCreate, GuildUpdate, Guild]
):
    repository: IGuildRepository = inject.attr(IGuildRepository)
