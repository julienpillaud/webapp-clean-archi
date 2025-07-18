import json
import logging.config
from typing import Any

from celery.signals import after_setup_logger

from app.core.config import Settings
from app.infrastructure.celery_task_queue.app import create_celery_app

settings = Settings()
celery_app = create_celery_app(settings=settings)
celery_app.autodiscover_tasks(["app.infrastructure.celery_task_queue.tasks"])


@after_setup_logger.connect
def setup_loggers(logger: logging.Logger, *args: Any, **kwargs: Any) -> None:
    with open("app/core/logging/config.json") as file:
        logging_config = json.load(file)
    logging.config.dictConfig(logging_config)
