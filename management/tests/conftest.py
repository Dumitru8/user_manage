import asyncio
import json
from datetime import datetime

import pytest
from fastapi.testclient import TestClient
from httpx import AsyncClient
from sqlalchemy import insert

from management.database import Base, async_session_maker, engine
from management.main import app as fastapi_app
from management.users.models import Group, User


@pytest.fixture(scope="session", autouse=True)
async def prepare_database():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    def open_mock_json(model: str):
        with open(f"management/tests/mock_{model}.json", encoding="utf-8") as file:
            return json.load(file)

    groups = open_mock_json("groups")
    users = open_mock_json("users")

    for user in users:
        user["created_at"] = datetime.strptime(user["created_at"], "%Y-%m-%d")
        user["modified_at"] = datetime.strptime(user["modified_at"], "%Y-%m-%d")

    for group in groups:
        group["created_at"] = datetime.strptime(group["created_at"], "%Y-%m-%d")

    async with async_session_maker() as session:
        for Model, values in [
            (Group, groups),
            (User, users),
        ]:
            query = insert(Model).values(values)
            await session.execute(query)

        await session.commit()


@pytest.fixture(scope="session")
def event_loop(request):
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="function")
async def ac():
    async with AsyncClient(app=fastapi_app, base_url="http://test") as ac:
        yield ac


@pytest.fixture(scope="function")
async def authenticated_ac():
    async with AsyncClient(app=fastapi_app, base_url="http://test") as ac:
        login_data = {"username": "testing", "password": "testing"}
        await ac.post("/auth/login", data=login_data)
        yield ac
