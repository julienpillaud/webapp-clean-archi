from typing import Any

from app.core.config import Settings
from app.domain.interfaces.task_queue import Task, TaskQueueProtocol
from app.infrastructure.celery_task_queue.app import create_celery_app


class CeleryTaskQueue(TaskQueueProtocol):
    def __init__(self, settings: Settings) -> None:
        self.celery_app = create_celery_app(settings=settings)

    @staticmethod
    def task(
        func_name: str,
        func_args: tuple[Any, ...] = (),
        func_kwargs: dict[str, Any] | None = None,
    ) -> Task:
        return Task(
            func_name=func_name,
            func_args=func_args,
            func_kwargs=func_kwargs or {},
        )

    def enqueue(self, task: Task, timeout: int = 60) -> str:
        result = self.celery_app.send_task(
            name="execute_domain_command",
            args=(task.func_name, *task.func_args),
            kwargs=task.func_kwargs,
            soft_time_limit=timeout,
        )
        return result.id
