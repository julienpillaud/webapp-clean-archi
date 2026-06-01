from app.api.app import create_fastapi_app
from app.dependencies.settings import get_settings

settings = get_settings()

app = create_fastapi_app(settings=settings)
