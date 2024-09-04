from typing import Optional, List, Tuple
from src.db import ISettingRepository, SettingOrm
from src.entities import Setting, SettingCreate, SettingUpdate
from .base import GenericService, IGenericService
from abc import ABC, abstractmethod, ABCMeta
import inject


class ISettingService(
    IGenericService[SettingOrm, SettingCreate, SettingUpdate, Setting],
    metaclass=ABCMeta,
):
    pass


class SettingService(
    ISettingService, GenericService[SettingOrm, SettingCreate, SettingUpdate, Setting]
):
    repository: ISettingRepository = inject.attr(ISettingRepository)
