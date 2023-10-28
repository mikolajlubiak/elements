from sqlalchemy import (
        Integer,
        String,
        )
from sqlalchemy.orm import (
        DeclarativeBase,
        Mapped,
        mapped_column,
        )
from typing import List, Optional
import datetime


class Base(DeclarativeBase):
    __abstract__ = True
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)


class User(Base):
    __tablename__ = "users"
    login: Mapped[str] = mapped_column(String(64))
    password: Mapped[str] = mapped_column(String(128))
