from faststream import FastStream
from faststream.rabbit import RabbitBroker
from faststream.rabbit.opentelemetry import RabbitTelemetryMiddleware

from app.core.config import Settings
from app.event_handler.router import router


def create_broker(settings: Settings) -> RabbitBroker:
    broker = RabbitBroker(
        str(settings.rabbitmq_dsn),
        middlewares=(RabbitTelemetryMiddleware(),),
    )
    broker.include_router(router)
    return broker


def create_faststream_app(settings: Settings) -> FastStream:
    broker = create_broker(settings=settings)
    return FastStream(broker)
