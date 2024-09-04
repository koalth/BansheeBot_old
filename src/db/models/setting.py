from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime
from typing import List, Optional
from ..base import Base


class SettingOrm(Base):
    __tablename__ = "settings"

    discord_guild_id: Mapped[str] = mapped_column(index=True)

    default_region: Mapped[Optional[str]] = mapped_column(nullable=True)
    default_realm: Mapped[Optional[str]] = mapped_column(nullable=True)

    admin_role_id: Mapped[Optional[str]] = mapped_column(nullable=True)
    raider_role_id: Mapped[Optional[str]] = mapped_column(nullable=True)
