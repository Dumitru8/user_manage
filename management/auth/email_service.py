import os

from dotenv import load_dotenv
from fastapi import HTTPException
from fastapi_mail import ConnectionConfig, FastMail, MessageSchema, MessageType
from starlette.responses import JSONResponse

load_dotenv()

conf = ConnectionConfig(
    MAIL_USERNAME=os.environ.get("MAIL_USERNAME"),
    MAIL_PASSWORD=os.environ.get("MAIL_PASSWORD"),
    MAIL_FROM=os.environ.get("MAIL_FROM"),
    MAIL_PORT=os.environ.get("MAIL_PORT"),
    MAIL_SERVER=os.environ.get("MAIL_SERVER"),
    MAIL_FROM_NAME=os.environ.get("MAIL_FROM_NAME"),
    MAIL_STARTTLS=True,
    MAIL_SSL_TLS=False,
    USE_CREDENTIALS=True,
    VALIDATE_CERTS=True,
)


fastmail = FastMail(conf)


def generate_reset_link():
    return "http://127.0.0.1:8000/auth/reset-password-data"


async def send_password_reset_email_service(email):
    reset_link = generate_reset_link()
    message = MessageSchema(
        subject="Password Reset Link",
        recipients=email.dict().get("email"),
        body=f"Click the following link to reset your password: {reset_link}",
        subtype=MessageType.html,
    )
    try:
        await fastmail.send_message(message)
        return JSONResponse(status_code=200, content={"message": "email has been sent"})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
