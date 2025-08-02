from typing import Annotated

from app.core.config import Settings
from app.core.context.context import Context
from app.core.dependencies import Dependency
from app.domain.context import ContextProtocol
from app.domain.domain import Domain


def get_settings() -> Settings:
    return Settings()


def get_context(
    settings: Annotated[Settings, Dependency(get_settings)],
) -> ContextProtocol:
    return Context(settings=settings)


def get_domain(
    context: Annotated[ContextProtocol, Dependency(get_context)],
) -> Domain:
    return Domain(context=context)
