from .base import GenericRepository
from .interfaces import ICharacterRepository
from ..models.character import CharacterOrm
from src.entities import Character, CharacterCreate, CharacterUpdate


class CharacterRepository(
    GenericRepository[CharacterOrm, CharacterCreate, CharacterUpdate, Character],
    ICharacterRepository,
):
    def __init__(self):
        super().__init__(CharacterOrm, Character)
