import uuid

import pytest

from management.users.service import UserService


@pytest.mark.parametrize(
    "user_id,email,is_present",
    [
        (uuid.UUID("2f006a7e-9c29-468f-b7ac-3aec0a990e81"), "test@test.com", True),
        (uuid.UUID("c2c18efd-8223-476a-8afa-7d2fc8df2723"), "dell@dell.com", True),
        (uuid.UUID("95b3bb19-6b5b-4f25-a05a-35ad56d9b9c8"), "abc@gmail.com", False),
    ],
)
async def test_get_by_id(user_id, email, is_present):
    user = await UserService.get_by_id(user_id)
    if is_present:
        assert user
        assert user.id == user_id
        assert user.email == email
    else:
        assert not user
