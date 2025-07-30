from cleanstack.exceptions import DomainError

from app.domain.context import ContextProtocol
from app.domain.exceptions import CustomError


class UnexpectedError(Exception):
    pass


class UnexpectedDomainError(DomainError):
    pass


def benchmark_command(context: ContextProtocol) -> str:
    return ""


def custom_error_command(context: ContextProtocol) -> None:
    raise CustomError("Custom error")


def unexpected_error_command(context: ContextProtocol) -> None:
    raise UnexpectedError("Unexpected error")


def unexpected_domain_error_command(context: ContextProtocol) -> None:
    raise UnexpectedDomainError("Unexpected domain error")


def run_task_command(context: ContextProtocol) -> str:
    return context.task_queue.enqueue(
        task=context.task_queue.task("task_to_run"),
        timeout=10,
    )


def task_to_run_command(context: ContextProtocol) -> str:
    return "Task to run executed successfully"
