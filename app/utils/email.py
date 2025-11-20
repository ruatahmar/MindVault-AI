from fastapi_mail import FastMail, MessageSchema, ConnectionConfig, MessageType
from app.config import settings 

conf = ConnectionConfig(
    MAIL_USERNAME = settings.EMAIL,
    MAIL_PASSWORD = settings.EMAIL_APP_PASSWORD,
    MAIL_FROM = settings.EMAIL,
    MAIL_PORT = 587,
    MAIL_SERVER = "smtp.gmail.com",
    MAIL_FROM_NAME="ADMIN",
    MAIL_STARTTLS = True,
    MAIL_SSL_TLS = False,
    USE_CREDENTIALS = True,
    VALIDATE_CERTS = True
)

async def send_reset_email(email: str, token: str):
    reset_link = f"http://127.0.0.1:8000/reset-password?token={token}"
    message = MessageSchema(
        subject="Password reset",
        recipients=[email],
        body=f"Click the link to reset your password: {reset_link}",
        subtype="plain"
    )
    fm = FastMail(conf)
    await fm.send_message(message)
    