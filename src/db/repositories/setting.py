from .base import GenericRepository
from .interfaces import ISettingRepository
from .mocks import MockGenericRepository
from ..models.setting import SettingOrm
from src.entities import Setting, SettingCreate, SettingUpdate


class SettingRepository(
    GenericRepository[SettingOrm, SettingCreate, SettingUpdate, Setting],
    ISettingRepository,
):
    def __init__(self):
        super().__init__(SettingOrm, Setting)


class SettingMockRepository(
    MockGenericRepository[SettingOrm, SettingCreate, SettingUpdate, Setting],
    ISettingRepository,
):
    def __init__(self):
        super().__init__(SettingOrm, Setting)
