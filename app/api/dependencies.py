from functools import lru_cache
from typing import Annotated

from fastapi import Depends

from app.core.config import Settings
from app.core.context.sql import Context
from app.domain.domain import Domain, TransactionalContextProtocol


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings(_env_file=".env")


def get_context() -> TransactionalContextProtocol:
    return Context()


def get_domain(
    context: Annotated[TransactionalContextProtocol, Depends(get_context)],
) -> Domain:
    return Domain(context=context)
