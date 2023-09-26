import uuid

from fastapi import HTTPException

from management.database import async_session_maker
from management.users.models import User
from management.users.enum import Role
from sqlalchemy import select, insert, update, delete, asc, desc


class UserData:
    @classmethod
    async def get_all_users(
        cls, page_nr, limit, filter_by_name, sort_by, ascending, current_user_id
    ):
        current_user = await UserData.get_by_id(current_user_id)
        if current_user.role not in (Role.ADMIN, Role.MODERATOR):
            raise HTTPException(
                status_code=403, detail="Have no access. Admin and moderator only"
            )
        offset = (page_nr - 1) * limit
        order = None
        if sort_by == "name":
            order = asc(User.name) if ascending else desc(User.name)
        elif sort_by == "surname":
            order = asc(User.surname) if ascending else desc(User.surname)
        elif sort_by == "email":
            order = asc(User.email) if ascending else desc(User.email)
        elif sort_by == "username":
            order = asc(User.username) if ascending else desc(User.username)
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
                        status_code=403, detail="Have no access.Moderator and users has to be same group"
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
    async def find_user_or_none(cls, **filter_by):
        async with async_session_maker() as session:
            query = select(User).filter_by(**filter_by)
            result = await session.execute(query)
            return result.scalar_one_or_none()

    @classmethod
    async def get_by_id(cls, model_id: uuid.UUID):
        async with async_session_maker() as session:
            query = select(User).filter_by(id=model_id)
            result = await session.execute(query)
            return result.scalar_one_or_none()

    @classmethod
    async def add(cls, **data):
        query = insert(User).values(**data)
        async with async_session_maker() as session:
            result = await session.execute(query)
            await session.commit()

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
