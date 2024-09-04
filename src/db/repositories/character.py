from .base import GenericRepository
from .mocks import MockGenericRepository
from .interfaces import ICharacterRepository
from ..models.character import CharacterOrm
from src.entities import Character, CharacterCreate, CharacterUpdate


class CharacterRepository(
    GenericRepository[CharacterOrm, CharacterCreate, CharacterUpdate, Character],
    ICharacterRepository,
):
    def __init__(self):
        super().__init__(CharacterOrm, Character)


class CharacterMockRepository(
    MockGenericRepository[CharacterOrm, CharacterCreate, CharacterUpdate, Character],
    ICharacterRepository,
):
    def __init__(self):
        super().__init__(CharacterOrm, Character)
