from faststream.rabbit import RabbitBroker

from app.core.config import Settings
from app.infrastructure.event_publisher.logger import logger


class RabbitMQProvider:
    _broker: RabbitBroker | None = None

    @classmethod
    def init(cls, settings: Settings, /) -> None:
        if cls._broker is None:
            logger.debug("Initializing RabbitMQ broker")
            cls._broker = RabbitBroker(str(settings.rabbitmq_dsn))

    @classmethod
    def get_broker(cls) -> RabbitBroker:
        if cls._broker is None:
            raise RuntimeError("Not initialized.")
        return cls._broker
