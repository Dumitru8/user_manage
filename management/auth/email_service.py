from fastapi import HTTPException
from management.auth.aws_boto3 import ses


def generate_reset_link():
    return "http://127.0.0.1:8000/auth/reset-password-data"


def send_reset_email(email: str, reset_link: str) -> None:
    subject = "Password Reset Link"
    recipients = [email]
    message_body = f"Click the following link to reset your password: {reset_link}"
    try:
        response = ses.send_email(
            Source="testapitestapi4@gmail.com",
            Destination={"ToAddresses": recipients},
            Message={
                "Subject": {"Data": subject},
                "Body": {"Text": {"Data": message_body}},
            },
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
