from celery import Celery
from .core.config import broker_settings

celery = Celery(__name__)
celery.conf.broker_url = broker_settings.CELERY_BROKER_URL
celery.conf.result_backend = broker_settings.CELERY_RESULT_BACKEND

celery.autodiscover_tasks(["app.tasks"])

@celery.task(name="example_task")
def example_task(name:str):
    return f"Hello, {name}!"