from datetime import datetime
from pydantic import EmailStr
from pydantic_extra_types.phone_numbers import PhoneNumber
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from enum import Enum

from sqlalchemy.orm import declarative_base

Base = declarative_base()


class Group(Base):
    __tablename__ = "groups"

    id: int = Column(Integer, primary_key=True)
    name: str = Column(String(50), nullable=False)
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
    phone_number: PhoneNumber = Column(PhoneNumber, nullable=False)
    email: EmailStr = Column(EmailStr, nullable=False)
    role: Role = Column(Enum(Role), default=Role.USER)
    group: Group = Column(ForeignKey(Group.name), nullable=False)
    s3_path: str = Column(String, nullable=False)
    is_blocked: bool = Column(Boolean, default=False)
    created_at: datetime = Column(DateTime, default=datetime.utcnow)
    modified_at: datetime = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
