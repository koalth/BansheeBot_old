import inject
from src.config import config
from src.raiderIO import IRaiderIOClient, RaiderIOClient
from src.services import ISettingsService, SettingsService

def base_config(binder: inject.Binder):

    binder.bind(
        IRaiderIOClient,
        RaiderIOClient(
            config.API_URL,
        ),
    )

    binder.bind(ISettingsService, SettingsService)


inject.configure(base_config, allow_override=True, clear=True)
