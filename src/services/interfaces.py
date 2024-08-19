from src.injector import inject

from src.db import CharacterRepository


class ICharacterService:

    repository: CharacterRepository = inject.attr(CharacterRepository)
