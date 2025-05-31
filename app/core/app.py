from app.api.app import create_app
from app.core.config import Settings
from app.core.context.utils import initialize_context

settings = Settings(_env_file=".env")
initialize_context(settings=settings)
app = create_app(settings=settings)
