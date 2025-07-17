from pathlib import Path

from celery import Celery

from app.core.config import Settings

project_dir = Path(__file__).parents[2]
settings = Settings(_env_file=project_dir / ".env")
celery_app = Celery("webapp_clean_archi", broker=str(settings.broker_dsn))
celery_app.autodiscover_tasks(["app.infrastructure.celery_task_queue.tasks"])
