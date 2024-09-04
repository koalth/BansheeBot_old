import inject
from loguru import logger
from src.entities import Character, CharacterCreate, CharacterUpdate
from src.external import IRaiderIOClient, CharacterResponse
from .base import GenericService, IGenericService
from src.db import ICharacterRepository, CharacterOrm
from abc import abstractmethod, ABCMeta


class ICharacterService(
    IGenericService[CharacterOrm, CharacterCreate, CharacterUpdate, Character],
    metaclass=ABCMeta,
):
    pass


class CharacterService(
    ICharacterService,
    GenericService[CharacterOrm, CharacterCreate, CharacterUpdate, Character],
):
    repository: ICharacterRepository = inject.attr(ICharacterRepository)
