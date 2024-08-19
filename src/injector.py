import inject

from src.db import GuildRepository, CharacterRepository
from src.services import GuildService, CharacterService


def config(binder: inject.Binder):
    binder.bind(GuildRepository, GuildRepository())
    binder.bind(CharacterRepository, CharacterRepository())

    binder.bind(GuildService, GuildService())
    binder.bind(CharacterService, CharacterService())


inject.configure_once(config)
