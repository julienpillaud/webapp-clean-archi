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
    ) -> Task:
        return Task(
            func_name=func_name,
            func_args=func_args,
            func_kwargs=func_kwargs or {},
        )

    def enqueue(self, task: Task, timeout: int = 60) -> str: ...
