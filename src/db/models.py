from sqlalchemy import ForeignKey, DateTime
from sqlalchemy.orm import DeclarativeBase, relationship, Mapped, mapped_column

from sqlalchemy.ext.asyncio import AsyncAttrs
from datetime import datetime
from typing import List


class Base(AsyncAttrs, DeclarativeBase):
    pass
