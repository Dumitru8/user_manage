from datetime import datetime

from httpx import AsyncClient

from management.users.service import UserService


async def test_add_and_get_user():
    new_user_data = {
        "name": "steve",
        "surname": "steve",
        "username": "steve",
        "phone_number": "+19248615323",
        "email": "steve@gmail.com",
        "password": "steve",
        "role": "USER",
        "group_id": 1,
        "s3_path": "steve",
        "is_blocked": False,
        "created_at": datetime.strptime("2023-10-10T16:31:52", "%Y-%m-%dT%H:%M:%S"),
        "modified_at": datetime.strptime("2023-10-10T16:31:52", "%Y-%m-%dT%H:%M:%S"),
    }
    new_user = await UserService.add_user(**new_user_data)

    found_user = await UserService.find_user_or_none(data=new_user_data["name"])

    assert found_user is not None
    assert found_user.name == "steve"

