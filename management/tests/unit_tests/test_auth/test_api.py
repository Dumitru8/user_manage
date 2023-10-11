import pytest
from httpx import AsyncClient


async def test_healthcheck(ac):
    response = await ac.get("/healthcheck")
    assert response.status_code == 200


@pytest.mark.parametrize(
    "id,name,surname,username,phone_number,email,password,role,group_id"
    ",s3_path,is_blocked,created_at,modified_at,status_code",
    [
        (
            "f47ac10b-58cc-4372-a567-0e02b2c3d479",
            "arnold",
            "arnold",
            "arnold",
            "+1234567890",
            "arnold@gmail.com",
            "arnold",
            "USER",
            1,
            "arnold",
            False,
            "2023-10-09T20:23:47",
            "2023-10-09T20:23:47",
            200,
        ),
        (
            "6ba7b810-9dad-11d1-80b4-00c04fd430c8",
            "Elvis",
            "Elvis",
            "Elvis",
            "+12345234190",
            "Elvis",
            "Elvis",
            "USER",
            1,
            "Elvis",
            "False",
            "2023-10-09T20:23:47",
            "2023-10-09T20:23:47",
            422,
        ),
    ],
)
async def test_signup(
    id,
    name,
    surname,
    username,
    phone_number,
    email,
    password,
    role,
    group_id,
    s3_path,
    is_blocked,
    created_at,
    modified_at,
    status_code,
    ac: AsyncClient,
):
    response = await ac.post(
        "/auth/signup",
        json={
            "id": id,
            "name": name,
            "surname": surname,
            "username": username,
            "phone_number": phone_number,
            "email": email,
            "password": password,
            "role": role,
            "group_id": group_id,
            "s3_path": s3_path,
            "is_blocked": is_blocked,
            "created_at": created_at,
            "modified_at": modified_at,
        },
    )

    assert response.status_code == status_code


@pytest.mark.parametrize(
    "username,password,status_code",
    [
        ("testing", "testing", 200),
        ("no_exist", "no_exist", 401),
        ("no_exist", True, 401),
    ],
)
async def test_login(username, password, status_code, ac: AsyncClient):
    response = await ac.post(
        "/auth/login", data={"username": username, "password": password}
    )
    assert response.status_code == status_code
