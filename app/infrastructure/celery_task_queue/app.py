from celery import Celery

from app.core.config import Settings


def create_celery_app(settings: Settings) -> Celery:
    return Celery("webapp_clean_archi", broker=str(settings.broker_dsn))
