from typing import Any, Protocol

from pydantic import BaseModel


class Task(BaseModel):
    func_name: str
    func_args: tuple[Any, ...] = ()
    func_kwargs: dict[str, Any] = {}


class TaskQueueProtocol(Protocol):
    @staticmethod
    def task(
        func_name: str,
        func_args: tuple[Any, ...] = (),
        func_kwargs: dict[str, Any] | None = None,
    ) -> Task: ...
    def enqueue(self, task: Task, timeout: int = 60) -> str: ...
