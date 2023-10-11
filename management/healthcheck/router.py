from fastapi import APIRouter
from fastapi.responses import JSONResponse


router = APIRouter(
    prefix="/healthcheck",
    tags=["Healthcheck"],
)


@router.get("")
async def healthcheck():
    return JSONResponse({'message': 'Successful request!'}, status_code=200)
