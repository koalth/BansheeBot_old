from src.db import CharacterOrm, GenericRepository, IGenericRepository
from src.entities import Character, CharacterCreate, CharacterUpdate
from abc import ABCMeta, abstractmethod


class ICharacterRepository(
    IGenericRepository[CharacterOrm, CharacterCreate, CharacterUpdate, Character],
    metaclass=ABCMeta,
):
    pass


class CharacterRepository(
    ICharacterRepository,
    GenericRepository[CharacterOrm, CharacterCreate, CharacterUpdate, Character],
):
    def __init__(self):
        super().__init__(CharacterOrm, Character)
