import uuid
from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, ConfigDict, EmailStr


class SToken(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str


class SUserId(BaseModel):
    user_id: uuid.UUID


class SUserEmail(BaseModel):
    email: EmailStr


class SUsername(BaseModel):
    username: str


class SResetPass(BaseModel):
    email: EmailStr
    new_password: str


class SEmailSchema(BaseModel):
    email: List[EmailStr]
