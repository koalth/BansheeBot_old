import inject

from src.db import GuildRepository, CharacterRepository


def config(binder: inject.Binder):
    binder.bind(GuildRepository, GuildRepository())


inject.configure_once(config)
