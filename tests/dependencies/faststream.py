from typing import Annotated

from cleanstack.infrastructure.mongodb.uow import MongoDBContext, MongoDBUnitOfWork
from cleanstack.infrastructure.sql.uow import SQLUnitOfWork
from fast_depends import Depends, dependency_provider

from app.core.config import Settings
from app.dependencies.faststream.dependencies import get_context
from app.dependencies.faststream.mongo import get_mongo_context, get_mongo_uow
from app.dependencies.faststream.sql import get_sql_uow
from app.dependencies.settings import get_settings
from tests.context import ContextTest
from tests.dependencies.dependencies import get_settings_override


def get_context_override(
    settings: Annotated[Settings, Depends(get_settings_override)],
    sql_uow: Annotated[SQLUnitOfWork, Depends(get_sql_uow)],
    mongo_context: Annotated[MongoDBContext, Depends(get_mongo_context)],
    mongo_uow: Annotated[MongoDBUnitOfWork, Depends(get_mongo_uow)],
) -> ContextTest:
    return ContextTest(
        settings=settings,
        sql_uow=sql_uow,
        mongo_context=mongo_context,
        mongo_uow=mongo_uow,
    )


def apply_faststream_overrides() -> None:
    dependency_provider.override(get_settings, get_settings_override)
    dependency_provider.override(get_context, get_context_override)
