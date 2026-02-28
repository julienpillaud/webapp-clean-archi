from functools import lru_cache
from typing import Annotated

from cleanstack.infrastructure.sql.uow import SQLContext, SQLUnitOfWork
from fast_depends import Depends

from app.core.config import Settings
from app.dependencies.settings import get_settings


@lru_cache(maxsize=1)
def get_sql_context(settings: Annotated[Settings, Depends(get_settings)]) -> SQLContext:
    return SQLContext.from_settings(url=str(settings.postgres_dsn))


def get_sql_uow(
    context: Annotated[SQLContext, Depends(get_sql_context)],
) -> SQLUnitOfWork:
    return SQLUnitOfWork(context=context)
