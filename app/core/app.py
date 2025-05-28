from app.api.app import create_app
from app.api.dependencies import get_settings
from app.core.context.sql import Context

settings = get_settings()
Context.initialize(settings=settings)
app = create_app(settings=settings)
