from typing import List
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig,MessageType, NameEmail
from src.Auth.Schema import Address
from src.config import configs


mail_config=ConnectionConfig(
    MAIL_USERNAME=configs.MAIL_USERNAME,
    MAIL_PASSWORD=configs.MAIL_PASSWORD,
    MAIL_FROM=configs.MAIL_FROM,
    MAIL_PORT=587,
    MAIL_SERVER=configs.MAIL_SERVER,
    MAIL_FROM_NAME=configs.MAIL_FROM_NAME,
    MAIL_STARTTLS=True,
    MAIL_SSL_TLS=False,
    USE_CREDENTIALS=True,
    VALIDATE_CERTS=True,
    )

mail=FastMail(mail_config)

def create_message(subject, body, recipients: List[str]):
    message = MessageSchema(
        subject=subject,
        recipients=[NameEmail(name="User",email=recipient.strip().lower()) for recipient in recipients],
        body=body,
        subtype=MessageType.html
    )
    return message