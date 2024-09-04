from src.db import SettingOrm, GenericRepository, IGenericRepository
from src.entities import Setting, SettingCreate, SettingUpdate
from abc import ABCMeta


class ISettingRepository(
    IGenericRepository[SettingOrm, SettingCreate, SettingUpdate, Setting],
    metaclass=ABCMeta,
):
    pass


class SettingRepository(
    ISettingRepository,
    GenericRepository[SettingOrm, SettingCreate, SettingUpdate, Setting],
):
    def __init__(self):
        super().__init__(SettingOrm, Setting)
