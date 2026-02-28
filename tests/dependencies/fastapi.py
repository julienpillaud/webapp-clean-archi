from typing import Annotated

from cleanstack.infrastructure.mongodb.uow import MongoDBContext, MongoDBUnitOfWork
from cleanstack.infrastructure.sql.uow import SQLUnitOfWork
from fastapi import Depends, FastAPI

from app.core.config import Settings
from app.dependencies.fastapi.dependencies import get_context
from app.dependencies.fastapi.mongo import get_mongo_context, get_mongo_uow
from app.dependencies.fastapi.sql import get_sql_uow
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


def apply_fastapi_overrides(app: FastAPI) -> None:
    app.dependency_overrides[get_settings] = get_settings_override
    app.dependency_overrides[get_context] = get_context_override
