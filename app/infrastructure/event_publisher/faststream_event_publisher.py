import asyncio

from app.core.config import Settings
from app.domain.interfaces.event_publisher import Event, EventPublisherProtocol
from app.infrastructure.event_publisher.provider import RabbitMQProvider


class FastStreamEventPublisher(EventPublisherProtocol):
    def __init__(self, settings: Settings):
        RabbitMQProvider.init(settings)
        self.broker = RabbitMQProvider.get_broker()

    async def _publish(self, events: list[Event]) -> None:
        async with self.broker as broker:
            tasks = [
                broker.publish(message=event.message, queue=event.queue)
                for event in events
            ]
            await asyncio.gather(*tasks)

    def publish(self, events: list[Event]) -> None:
        asyncio.run(self._publish(events=events))
