from fastapi import FastAPI
from typing import Optional
from datetime import datetime
from pydantic import BaseModel, EmailStr
from pydantic_extra_types.phone_numbers import PhoneNumber


app = FastAPI()


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
