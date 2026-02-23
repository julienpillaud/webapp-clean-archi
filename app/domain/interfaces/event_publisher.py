from typing import Any, Protocol

from pydantic import BaseModel


class Event(BaseModel):
    queue: str
    message: Any


class EventPublisherProtocol(Protocol):
    def publish(self, events: list[Event]) -> None: ...
