from app.api.app import app_factory
from app.core.config import Settings
from app.core.context import Context
from app.domain.domain import Domain

settings = Settings(_env_file=".env")  # type: ignore

context = Context(settings=settings)

domain = Domain(context=context)

app = app_factory(domain=domain)
