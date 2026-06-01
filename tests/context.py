import asyncio
from functools import cached_property
from typing import Annotated

from fastapi import Depends
from faststream.rabbit import TestRabbitBroker
from sqlalchemy.orm import Session

from app.core.config import Settings
from app.core.context import Context
from app.dependencies.fastapi.dependencies import get_session
from app.domain.interfaces.event_publisher import Event, EventPublisherProtocol
from app.event_handler.app import create_broker
from tests.plugins.settings import get_settings_override


class InMemoryEventPublisher(EventPublisherProtocol):
    def __init__(self, settings: Settings) -> None:
        broker = create_broker(settings=settings)
        self.broker = TestRabbitBroker(broker)

    async def _publish(self, events: list[Event]) -> None:
        async with self.broker as broker:
            tasks = [
                broker.publish(message=event.message, queue=event.queue)
                for event in events
            ]
            await asyncio.gather(*tasks)

    def publish(self, events: list[Event]) -> None:
        asyncio.run(self._publish(events=events))


class ContextTest(Context):
    @cached_property
    def event_publisher(self) -> EventPublisherProtocol:
        return InMemoryEventPublisher(settings=self.settings)


def get_context_override(
    settings: Annotated[Settings, Depends(get_settings_override)],
    session: Annotated[Session, Depends(get_session)],
) -> ContextTest:
    return ContextTest(settings=settings, session=session)
