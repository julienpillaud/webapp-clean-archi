import logging

import logfire

from app.api.app import create_app
from app.core.config import Settings
from app.core.context.sql import SqlContext

logger = logging.getLogger(__name__)

settings = Settings()
logger.info(f"Loading settings for {settings.environment} environment")
logfire.configure(
    send_to_logfire="if-token-present",
    token=settings.logfire_token,
    service_name=settings.project_name,
    service_version=settings.api_version,
    environment=settings.environment,
    console=False,
)
SqlContext.initialize(settings=settings)

app = create_app(settings=settings)
logfire.instrument_fastapi(app)
