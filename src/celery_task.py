from typing import List
from celery import Celery
from src.Mail import create_message,mail
from src.config import configs
from asgiref.sync import async_to_sync


celery_app=Celery(
    name='worker',
    broker=configs.CELERY_BROKER_URL,
    backend=configs.CELERY_RESULT_BACKEND)

celery_app.conf.update(
    task_serializer='json',
    accept_content=['json'],
    result_serializer='json',
    timezone='Asia/Kolkata',
    enable_utc=True
)

@celery_app.task(name='send_email')
def send_email(subject,recipients:List[str],body):
    message=create_message(subject=subject,body=body,recipients=recipients)
    async_to_sync(mail.send_message)(message)