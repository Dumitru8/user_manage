import uuid
from datetime import datetime

from pydantic import EmailStr
from sqlalchemy import (
    UUID,
    Boolean,
    Column,
    DateTime,
    Enum,
    ForeignKey,
    Integer,
    String,
)
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.orm import relationship, validates

from management.database import Base
from management.users.enum import Role


class Group(Base):
    __tablename__ = "groups"

    id: int = Column(Integer, primary_key=True)
    name: str = Column(String(50), nullable=False, unique=True)
    created_at: DateTime = Column(DateTime, default=datetime.now())

    users = relationship("User", back_populates="group")

    def __str__(self):
        return f"Group {self.name}"


class User(Base):
    __tablename__ = "users"

    id: int = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name: str = Column(String(50), nullable=False)
    surname: str = Column(String(50), nullable=False)
    username: str = Column(String(50), nullable=False)
    phone_number: str = Column(String(14), nullable=False)
    email: str = Column(String(50), nullable=False)
    password: str = Column(String(150), nullable=False)
    role: Role = Column(Enum(Role), default=Role.USER, nullable=False)
    group_id: Group = Column(ForeignKey(Group.id), nullable=False)
    s3_path: str = Column(String(255), nullable=False)
    is_blocked: bool = Column(Boolean, default=False)
    created_at: DateTime = Column(DateTime, default=datetime.now())
    modified_at: DateTime = Column(
        DateTime, default=datetime.now(), onupdate=datetime.now()
    )

    group = relationship("Group", back_populates="users")

    @validates("password")
    def validate_password(self, value):
        if len(value) < 8:
            raise ValueError("Password should be at least 8 symbols")
        return value
