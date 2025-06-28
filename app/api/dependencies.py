from functools import lru_cache
from typing import Annotated

from fastapi import Depends

from app.core.config import Settings
from app.core.context.utils import get_context
from app.domain.domain import Domain, TransactionalContextProtocol


@lru_cache(maxsize=1)
def get_settings(env_file: str | None = None) -> Settings:
    return Settings(_env_file=env_file)


def get_domain(
    context: Annotated[TransactionalContextProtocol, Depends(get_context)],
) -> Domain:
    return Domain(context=context)
