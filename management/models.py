from datetime import datetime
from typing import List

from pydantic import EmailStr
from pydantic_extra_types.phone_numbers import PhoneNumber
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from enum import Enum

from sqlalchemy.dialects.postgresql import ENUM
from sqlalchemy.orm import declarative_base

from database import Base


class Group(Base):
    __tablename__ = "groups"

    id: int = Column(Integer, primary_key=True)
    name: str = Column(String(50), nullable=False, unique=True)
    created_at: datetime = Column(DateTime, default=datetime.utcnow)


class Role(Enum):
    USER = "USER"
    ADMIN = "ADMIN"
    MODERATOR = "MODERATOR"


class User(Base):
    __tablename__ = "users"

    id: int = Column(Integer, primary_key=True, index=True)
    name: str = Column(String(50), nullable=False)
    surname: str = Column(String(50), nullable=False)
    username: str = Column(String(50), nullable=False)
    phone_number: str = Column(String(12), nullable=False)
    email: str = Column(String(50), nullable=False)
    role: Role = Column(ENUM(Role), default=Role.USER)
    group: Group = Column(ForeignKey(Group.name), nullable=False)
    s3_path: str = Column(String(255), nullable=False)
    is_blocked: bool = Column(Boolean, default=False)
    created_at: datetime = Column(DateTime, default=datetime.utcnow)
    modified_at: datetime = Column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )
