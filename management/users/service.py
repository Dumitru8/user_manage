import uuid

from fastapi import HTTPException
from sqlalchemy import asc, delete, desc, insert, select, update, or_

from management.database import async_session_maker
from management.users.enum import Role
from management.users.models import User


class UserService:
    @classmethod
    async def get_all_users(
        cls, page_nr, limit, filter_by_name, sort_by, ascending, current_user_id
    ):
        current_user = await UserService.get_by_id(current_user_id)
        if current_user.role not in (Role.ADMIN, Role.MODERATOR):
            raise HTTPException(
                status_code=403, detail="Have no access. Admin and moderator only"
            )
        offset = (page_nr - 1) * limit
        options = {
            "name": asc(User.name) if ascending else desc(User.name),
            "surname": asc(User.surname) if ascending else desc(User.surname),
            "email": asc(User.email) if ascending else desc(User.email),
            "username": asc(User.username) if ascending else desc(User.username)
        }
        order = options.get(sort_by)
        if current_user.role == Role.MODERATOR:
            async with async_session_maker() as session:
                query = (
                    select(User)
                    .filter(User.name == filter_by_name)
                    .filter(User.group_id == current_user.group_id)
                    .order_by(order)
                    .offset(offset)
                    .limit(limit)
                )
                users = await session.execute(query)
                result = users.scalars().all()
                if not result:
                    raise HTTPException(
                        status_code=403,
                        detail="Have no access.Moderator and users has to be same group",
                    )
                return result
        async with async_session_maker() as session:
            query = (
                select(User)
                .filter(User.name == filter_by_name)
                .order_by(order)
                .offset(offset)
                .limit(limit)
            )
            users = await session.execute(query)
            return users.scalars().all()

    @classmethod
    async def find_user_or_none(cls, data):
        async with async_session_maker() as session:
            query = select(User).filter(
                or_(
                    User.email == data,
                    User.username == data,
                    User.phone_number == data
                )
            )
            result = await session.execute(query)
            return result.scalar_one_or_none()

    @classmethod
    async def get_by_id(cls, model_id: uuid.UUID):
        async with async_session_maker() as session:
            query = select(User).filter_by(id=model_id)
            result = await session.execute(query)
            return result.scalar_one_or_none()

    @classmethod
    async def add_user(cls, **data):
        query = insert(User).values(**data).returning(User)
        async with async_session_maker() as session:
            result = await session.execute(query)
            await session.commit()
            user_mapping = result.mappings().first()
            return user_mapping["User"]

    @classmethod
    async def user_update(cls, user_id, **data):
        query = update(User).where(User.id == user_id).values(**data)
        async with async_session_maker() as session:
            result = await session.execute(query)
            await session.commit()

    @classmethod
    async def user_delete(cls, user_id):
        query = delete(User).where(User.id == user_id)
        async with async_session_maker() as session:
            result = await session.execute(query)
            await session.commit()
