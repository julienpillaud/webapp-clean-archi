from app.core.worker import celery_app
from app.domain.interfaces.task_queue import Task, TaskQueueProtocol


class CeleryTaskQueue(TaskQueueProtocol):
    def enqueue(self, task: Task, timeout: int = 60) -> str:
        result = celery_app.send_task(
            name="execute_domain_command",
            args=(task.func_name, *task.func_args),
            kwargs=task.func_kwargs,
            soft_time_limit=timeout,
        )
        return result.id
