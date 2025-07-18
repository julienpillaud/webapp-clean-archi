from app.core.config import Settings
from app.domain.interfaces.task_queue import Task, TaskQueueProtocol
from app.infrastructure.celery_task_queue.app import create_celery_app


class CeleryTaskQueue(TaskQueueProtocol):
    def __init__(self, settings: Settings) -> None:
        self.celery_app = create_celery_app(settings=settings)

    def enqueue(self, task: Task, timeout: int = 60) -> str:
        result = self.celery_app.send_task(
            name="execute_domain_command",
            args=(task.func_name, *task.func_args),
            kwargs=task.func_kwargs,
            soft_time_limit=timeout,
        )
        return result.id
