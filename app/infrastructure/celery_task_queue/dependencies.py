from typing import Annotated

from app.core.config import Settings
from app.core.context.sql import SqlContext
from app.core.dependencies import Dependency
from app.domain.domain import Domain, TransactionalContextProtocol


def get_settings() -> Settings:
    return Settings()


def get_context(
    settings: Annotated[Settings, Dependency(get_settings)],
) -> TransactionalContextProtocol:
    return SqlContext(settings=settings)


def get_domain(
    context: Annotated[TransactionalContextProtocol, Dependency(get_context)],
) -> Domain:
    return Domain(context=context)
