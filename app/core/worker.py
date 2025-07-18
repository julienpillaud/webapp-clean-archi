from app.core.config import Settings
from app.infrastructure.celery_task_queue.app import create_celery_app

settings = Settings()
celery_app = create_celery_app(settings=settings)
celery_app.autodiscover_tasks(["app.infrastructure.celery_task_queue.tasks"])
