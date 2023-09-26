import os

from dotenv import load_dotenv
from fastapi_mail import FastMail, ConnectionConfig

load_dotenv()

conf = ConnectionConfig(
    MAIL_USERNAME=os.environ.get('MAIL_USERNAME'),
    MAIL_PASSWORD=os.environ.get('MAIL_PASSWORD'),
    MAIL_FROM=os.environ.get('MAIL_FROM'),
    MAIL_PORT=os.environ.get('MAIL_PORT'),
    MAIL_SERVER=os.environ.get('MAIL_SERVER'),
    MAIL_FROM_NAME=os.environ.get('MAIL_FROM_NAME'),
    MAIL_STARTTLS=True,
    MAIL_SSL_TLS=False,
    USE_CREDENTIALS=True,
    VALIDATE_CERTS=True
)


fastmail = FastMail(conf)
