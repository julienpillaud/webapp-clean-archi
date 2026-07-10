from app.api.app import create_fastapi_app
from app.api.dependencies import get_settings

settings = get_settings()
app = create_fastapi_app(settings=settings)
