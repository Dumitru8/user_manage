from fastapi import APIRouter


router = APIRouter(
    prefix="/user",
    tags=["Users"],
)


@router.get("")
async def get_user():
    pass


@router.get("/{user_id}")
def get_user_id(user_id):
    pass


@router.patch("/{user_id}")
def patch_user2(user_id):
    pass
