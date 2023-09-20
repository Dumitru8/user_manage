import os

from fastapi import FastAPI, Request
from pydantic import BaseModel, EmailStr
from pydantic_extra_types.phone_numbers import PhoneNumber
import time
from management.logger import logger
from management.users.router import router as router_users

from management.settings import DevAppSettings, BaseAppSettings, TestAppSettings

app = FastAPI()

app.include_router(router_users)

current_environment = os.getenv('CURRENT_DEVELOPMENT')


@app.get("/healthcheck")
async def healthcheck():
    return {"message": "Hello World"}


class SSignup(BaseModel):
    name: str
    surname: str
    username: str
    phone_number: PhoneNumber
    email: EmailStr


@app.post("/auth/signup")
async def signup(sign: SSignup):
    pass


settings_ = {"development": DevAppSettings, "testing": TestAppSettings}
settings = settings_[current_environment]() if current_environment else BaseAppSettings()


@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    logger.info("Request handling time", extra={
        "process_time": round(process_time, 4)
    })
    return response
