from celery import Celery

from app.core.config import Settings


def create_celery_app(settings: Settings) -> Celery:
    return Celery(settings.project_name, broker=str(settings.broker_dsn))
