import logging
from functools import lru_cache
from typing import Annotated

from fastapi import Depends

from app.core.config import Settings
from app.core.context.sql import Context
from app.domain.domain import Domain, TransactionalContextProtocol

logger = logging.getLogger(__name__)


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    logger.info("Loading settings")
    return Settings(_env_file=".env")


def get_context(
    settings: Annotated[Settings, Depends(get_settings)],
) -> TransactionalContextProtocol:
    return Context(settings=settings)


def get_domain(
    context: Annotated[TransactionalContextProtocol, Depends(get_context)],
) -> Domain:
    return Domain(context=context)
