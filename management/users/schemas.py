import uuid
from datetime import datetime
from typing import Optional
from pydantic import constr, ConfigDict
from pydantic import BaseModel
from pydantic import EmailStr

from management.users.enum import Role


class SUser(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
        arbitrary_types_allowed=True
    )

    id: uuid.UUID
    name: str
    surname: str
    username: str
    phone_number: str
    email: EmailStr
    password: str
    role: Role
    group_id: int
    s3_path: str
    is_blocked: bool
    created_at: Optional[datetime]
    modified_at: Optional[datetime]


class SUserUpd(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
        arbitrary_types_allowed=True
    )

    name: str
    surname: str
    username: str
    phone_number: str
    modified_at: Optional[datetime]


