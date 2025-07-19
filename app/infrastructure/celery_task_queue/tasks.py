from typing import Any

from app.core.dependencies import DependencyContainer
from app.core.worker import celery_app
from app.infrastructure.celery_task_queue.dependencies import get_domain


@celery_app.task(name="execute_domain_command")
def execute_domain_command(*args: Any, **kwargs: Any) -> Any:
    command_name, *command_args = args
    domain = DependencyContainer.resolve(get_domain)
    method = getattr(domain, command_name)
    return method(*command_args, **kwargs)
