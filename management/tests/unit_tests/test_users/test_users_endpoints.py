import uuid

import pytest
from fastapi import Depends
from httpx import AsyncClient

from management.auth.auth import get_user_id_from_token, create_token
from management.users.service import UserData


async def test_get_me(ac: AsyncClient):
    auth_token = f"Bearer {create_token({'sub': '0c20a463-7ed8-4a22-aa01-97e4aef48760'}, flag=True)}"
    headers = {"Authorization": auth_token}

    response = await ac.get("/user/me", headers=headers)
    assert response.status_code == 200


async def test_delete_me(ac: AsyncClient):
    auth_token = f"Bearer {create_token({'sub': '0c20a463-7ed8-4a22-aa01-97e4aef48760'}, flag=True)}"
    headers = {"Authorization": auth_token}

    response = await ac.delete("/user/me", headers=headers)
    assert response.status_code == 200


async def test_update_me(ac: AsyncClient):
    auth_token = f"Bearer {create_token({'sub': 'a64984ee-3555-47c3-a286-f4f759e2d83e'}, flag=True)}"
    headers = {"Authorization": auth_token}

    response = await ac.patch("/user/me", headers=headers, json={
            "name": "nicetry_updated",
            "surname": "nicetry_updated",
            "username": "nicetry_updated",
            "phone_number": "+1233498240",
            "modified_at": "2023-10-11T10:24:39"
    })
    assert response.status_code == 200


async def test_update_user_with_privileges(ac: AsyncClient):
    auth_token = f"Bearer {create_token({'sub': '6533c16f-77da-46fc-9374-870612185300'}, flag=True)}"
    headers = {"Authorization": auth_token}
    response = await ac.patch("/user/ca600e1c-1b7a-4fd3-bb62-9f9c8db1d46f", headers=headers, json={
            "name": "Michael_updated",
            "surname": "Michael_updated",
            "username": "Michael_updated",
            "phone_number": "+1232342240",
            "modified_at": "2022-12-12T10:54:25"
    })
    assert response.status_code == 200


async def test_update_user_for_non_admin_role(ac: AsyncClient):
    auth_token = f"Bearer {create_token({'sub': '4ba5fdbb-29f2-422c-af3c-5eb8a3b38ec2'}, flag=True)}"
    headers = {"Authorization": auth_token}
    response = await ac.patch("/user/4a0a0f1d-17e3-49a9-9f8e-9357a07e379e", headers=headers, json={
            "name": "Michael_updated",
            "surname": "Michael_updated",
            "username": "Michael_updated",
            "phone_number": "+1232342240",
            "modified_at": "2022-12-12T10:54:25"
    })
    assert response.status_code == 403
