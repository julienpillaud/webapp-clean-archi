import logfire

from app.api.app import create_app
from app.api.dependencies import get_settings
from app.core.context.sql import SqlContext

settings = get_settings(env_file=".env")
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
