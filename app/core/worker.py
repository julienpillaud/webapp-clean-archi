import json
import logging.config
from typing import Any

import logfire
from celery.signals import after_setup_logger, worker_init, worker_ready

from app.core.config import Settings
from app.infrastructure.celery_task_queue.app import create_celery_app

logger = logging.getLogger(__name__)

settings = Settings()
celery_app = create_celery_app(settings=settings)
celery_app.autodiscover_tasks(["app.infrastructure.celery_task_queue.tasks"])


@worker_init.connect()
def init_worker(*args: Any, **kwargs: Any) -> None:
    logfire.configure(
        send_to_logfire="if-token-present",
        token=settings.logfire_token,
        service_name="worker",
        environment=settings.environment,
        console=False,
    )
    logfire.instrument_celery()


@after_setup_logger.connect
def setup_loggers(*args: Any, **kwargs: Any) -> None:
    with open("app/core/logging/config.json") as file:
        logging_config = json.load(file)
    logging.config.dictConfig(logging_config)


@worker_ready.connect
def on_worker_ready(*args: Any, **kwargs: Any) -> None:
    logger.debug(f"Loading settings for ENV {settings.environment}")
    logger.debug("Created Celery Worker")
