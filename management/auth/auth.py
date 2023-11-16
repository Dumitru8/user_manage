import os
from datetime import datetime, timedelta

import jwt
import redis
from dotenv import load_dotenv
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from pydantic import EmailStr

from management.users.service import UserService

load_dotenv()

redis_host = os.getenv("REDIS_HOST")
redis_port = int(os.getenv("REDIS_PORT"))

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")
redis_client = redis.Redis(host=redis_host, port=redis_port, db=0, decode_responses=True)

JWT_SECRET_KEY = os.getenv("SECRET_KEY")
JWT_ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv('ACCESS_TOKEN_EXPIRE_MINUTES', 60))
REFRESH_TOKEN_EXPIRE_MINUTES = int(os.getenv('REFRESH_TOKEN_EXPIRE_MINUTES', 60))


def get_password_hash(password: str) -> str:
    """Getting hash from password"""
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify if entered password hash equals hashed value"""
    return pwd_context.verify(
        secret=plain_password,
        hash=hashed_password
    )


def create_token(data: dict, flag: bool) -> str:
    """Create JWT token with encrypted data in payload"""
    token_expire = ACCESS_TOKEN_EXPIRE_MINUTES if flag else REFRESH_TOKEN_EXPIRE_MINUTES
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=token_expire)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, JWT_SECRET_KEY, JWT_ALGORITHM)
    return encoded_jwt


async def authenticate_user(data: (str, EmailStr), password: str):
    """Authenticate user using email, username or phone_number"""
    user = await UserService.find_user_or_none(data=data)
    if user and verify_password(password, user.password):
        return user
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)


async def get_user_id_from_token(token: str = Depends(oauth2_scheme)):
    """Getting user id from token and add to blacklist expired one"""
    try:
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])
        user_id = payload.get("sub")
        if user_id is None:
            raise HTTPException(status_code=400, detail="Invalid token")
        exp = payload.get("exp")
        if exp:
            redis_client.set(f"blacklist:{str(token)}", "1")
        return user_id
    except jwt.exceptions.DecodeError:
        raise HTTPException(status_code=400, detail="Invalid token")
