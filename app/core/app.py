import logfire

from app.api.app import create_fastapi_app
from app.core.config import Settings
from app.core.core import initialize_app
from app.core.logger import logger

settings = Settings()
logfire.configure(
    send_to_logfire="if-token-present",
    token=settings.logfire_token,
    service_name="app",
    service_version=settings.api_version,
    environment=settings.environment,
    console=False,
)
logger.debug(f"Loading settings for ENV {settings.environment}")
app = create_fastapi_app(settings=settings)
initialize_app(settings=settings)
logfire.instrument_fastapi(app, capture_headers=True, extra_spans=True)
