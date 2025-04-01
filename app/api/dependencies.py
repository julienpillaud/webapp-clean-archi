from functools import lru_cache
from typing import Annotated

from fastapi import Depends

from app.core.config import Settings
from app.core.context import Context
from app.domain.domain import Domain, TransactionalContextProtocol


@lru_cache
def get_settings() -> Settings:
    return Settings(_env_file=".env")  # type: ignore


def get_context(
    settings: Annotated[Settings, Depends(get_settings)],
) -> TransactionalContextProtocol:
    return Context(settings=settings)


def get_domain(
    context: Annotated[TransactionalContextProtocol, Depends(get_context)],
) -> Domain:
    return Domain(context=context)
