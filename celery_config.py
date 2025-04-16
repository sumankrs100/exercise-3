# app/celery_config.py
from celery import Celery

# Configure Celery with Redis backend
app = Celery('batch_processor',
             broker='redis://your-redis-server:6379/0',
             backend='redis://your-redis-server:6379/0')

# Optional configurations
app.conf.update(
    task_serializer='json',
    accept_content=['json'],
    result_serializer='json',
    timezone='UTC',
    enable_utc=True,
)
