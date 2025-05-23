from app.api.app import create_app
from app.api.dependencies import get_settings

settings = get_settings()
app = create_app(settings=settings)
