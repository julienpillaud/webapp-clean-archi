from fastapi import FastAPI

from app.core.config import Settings
from app.core.context import Context
from app.domain.domain import Domain


def initialize_app(settings: Settings, app: FastAPI) -> None:
    context = Context(settings=settings)
    domain = Domain(context=context)
    app.state.domain = domain
