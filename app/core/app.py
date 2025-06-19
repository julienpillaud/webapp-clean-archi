from app.api.app import create_app
from app.core.config import Settings
from app.core.context.sql import SqlContext

settings = Settings(_env_file=".env")
SqlContext.initialize(settings=settings)
app = create_app(settings=settings)
