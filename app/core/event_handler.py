from app.dependencies.settings import get_settings
from app.event_handler.app import create_faststream_app

settings = get_settings()
app = create_faststream_app(settings=settings)
