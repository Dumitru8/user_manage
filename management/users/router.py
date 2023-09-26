import uuid
from datetime import datetime
from typing import List

from fastapi import APIRouter, Depends, HTTPException

from management.auth.auth import get_user_id_from_token
from management.users.enum import Role
from management.users.schemas import SUser, SUserUpd
from management.users.service import UserData

router = APIRouter(
    prefix="/user",
    tags=["Users"],
)


@router.get("/me")
async def get_current_user(
    user_id: uuid.UUID = Depends(get_user_id_from_token),
) -> SUser:
    return await UserData.get_by_id(user_id)


@router.patch("/me")
async def update_current_user(
    user_data: SUserUpd,
    user_id: uuid.UUID = Depends(get_user_id_from_token),
):
    user = await UserData.get_by_id(user_id)
    await UserData.user_update(
        user_id,
        name=user_data.name,
        surname=user_data.surname,
        username=user_data.username,
        phone_number=user_data.phone_number,
        modified_at=datetime.now(),
    )
    return user


@router.delete("/me")
async def delete_current_user(user_id: uuid.UUID = Depends(get_user_id_from_token)):
    return await UserData.user_delete(user_id)


@router.patch("/{user_id}")
async def get_user_by_id(user_id: uuid.UUID, user_data: SUserUpd) -> SUser:
    user = await UserData.get_by_id(user_id)
    if user.role != Role.ADMIN:
        raise HTTPException(status_code=403, detail="Have no access. Admin only")
    await UserData.user_update(
        user_id,
        name=user_data.name,
        surname=user_data.surname,
        username=user_data.username,
        phone_number=user_data.phone_number,
        modified_at=datetime.now(),
    )
    return user


@router.get("s")
async def get_filtered_users(
    page: int,
    limit: int,
    filter_by_name: str,
    sort_by: str,
    ascending: bool,
    current_user_id: uuid.UUID = Depends(get_user_id_from_token),
) -> List[SUser]:
    return await UserData.get_all_users(page, limit, filter_by_name, sort_by, ascending, current_user_id)


@router.get("/{user_id}")
async def get_user_by_id(
    user_id: uuid.UUID, current_user_id: uuid.UUID = Depends(get_user_id_from_token)
) -> SUser:
    current_user = await UserData.get_by_id(current_user_id)
    user = await UserData.get_by_id(user_id)
    if current_user.role not in (Role.ADMIN, Role.MODERATOR):
        raise HTTPException(status_code=403, detail="Have no access. Admin and moderator only")
    if current_user.role in (Role.ADMIN, Role.MODERATOR):
        if current_user.group_id == user.group_id:
            return user
    raise HTTPException(status_code=403, detail="Have no access. Admin and moderator of same group only")