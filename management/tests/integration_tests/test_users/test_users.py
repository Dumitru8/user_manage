from datetime import datetime

from httpx import AsyncClient

from management.users.service import UserData


async def test_add_and_get_user():
    new_user = await UserData.add(
        name="steve",
        surname="steve",
        username="steve",
        phone_number="+19248615323",
        email="steive@gmail.com",
        password="steve",
        role="USER",
        group_id=1,
        s3_path="steve",
        is_blocked=False,
        created_at=datetime.strptime("2023-10-10T16:31:52", "%Y-%m-%dT%H:%M:%S"),
        modified_at=datetime.strptime("2023-10-10T16:31:52", "%Y-%m-%dT%H:%M:%S"),
    )
    assert new_user.username == "steve"
    #
    new_user = await UserData.find_user_or_none(username=new_user.username)
    #
    assert new_user is not None
