from functools import lru_cache
from typing import Annotated

from fastapi import Depends

from app.core.config import Settings
from app.dependencies.settings import get_settings
from app.infrastructure.sql.uow import SQLContext, SQLUnitOfWork


@lru_cache(maxsize=1)
def get_sql_context(settings: Annotated[Settings, Depends(get_settings)]) -> SQLContext:
    return SQLContext.from_settings(dsn=str(settings.postgres_dsn))


def get_sql_uow(
    context: Annotated[SQLContext, Depends(get_sql_context)],
) -> SQLUnitOfWork:
    return SQLUnitOfWork(context=context)
