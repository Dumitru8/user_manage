from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from fastapi_mail import MessageSchema, MessageType
from starlette.responses import JSONResponse

from management.auth.auth import (
    authenticate_user,
    create_token,
    get_password_hash,
    get_user_id_from_token,
)
from management.auth.email_service import fastmail, generate_reset_link, send_password_reset_email_service
from management.auth.schemas import SEmailSchema, SResetPass, SToken, SUserId
from management.users.schemas import SUser
from management.users.service import UserService

router = APIRouter(
    prefix="/auth",
    tags=["auth"],
)


@router.post("/signup", response_model=SUser)
async def signup_user(user_data: SUser):
    existing_user = await UserService.find_user_or_none(data=user_data.email)
    if existing_user:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY)
    hashed_password = get_password_hash(user_data.password)
    user = await UserService.add_user(
        email=user_data.email,
        password=hashed_password,
        name=user_data.name,
        surname=user_data.surname,
        username=user_data.username,
        phone_number=user_data.phone_number,
        role=user_data.role,
        group_id=user_data.group_id,
        s3_path=user_data.s3_path,
        is_blocked=user_data.is_blocked,
        created_at=user_data.created_at,
        modified_at=user_data.modified_at
    )
    return user


@router.post("/login", response_model=SToken)
async def login_user(user_data: OAuth2PasswordRequestForm = Depends()):
    user = await authenticate_user(user_data.username, user_data.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    access_token = create_token({"sub": str(user.id)}, flag=True)
    refresh_token = create_token({"sub": str(user.id)}, flag=False)
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
    }


@router.post("/refresh-token", response_model=SToken)
async def refresh_both_tokens(user_id: SUserId = Depends(get_user_id_from_token)):
    access_token = create_token({"sub": str(user_id)}, flag=True)
    refresh_token = create_token({"sub": str(user_id)}, flag=False)
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
    }


@router.post("/reset-password")
async def send_password_reset_email(email: SEmailSchema) -> JSONResponse:
    reset_link = generate_reset_link()
    message = MessageSchema(
        subject="Password Reset Link",
        recipients=email.dict().get("email"),
        body=f"Click the following link to reset your password: {reset_link}",
        subtype=MessageType.html,
    )
    try:
        await fastmail.send_message(message)
        return JSONResponse(status_code=200, content={"message": "email has been sent"})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/reset-password-data")
async def reset_password_data(user_data: SResetPass) -> JSONResponse:
    user = await UserService.find_user_or_none(data=user_data.email)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    await UserService.user_update(
        user.id, password=get_password_hash(user_data.new_password)
    )
    return JSONResponse(
        status_code=200, content={"message": "password has been updated"}
    )
