import inject
from src.config import config
from src.raiderIO import IRaiderIOClient, RaiderIOClient


def base_config(binder: inject.Binder):

    binder.bind(
        IRaiderIOClient,
        RaiderIOClient(
            config.API_URL,
        ),
    )


inject.configure(base_config, allow_override=True, clear=True)
