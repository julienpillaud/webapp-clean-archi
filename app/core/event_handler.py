import logfire

from app.core.config import Settings
from app.event_handler.app import create_faststream_app

settings = Settings()
logfire.configure(
    send_to_logfire="if-token-present",
    token=settings.logfire_token,
    service_name="worker",
    service_version=settings.api_version,
    environment=settings.environment,
    console=False,
)
app = create_faststream_app(settings=settings)
