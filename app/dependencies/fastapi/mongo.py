from functools import lru_cache
from typing import Annotated

from cleanstack.infrastructure.mongodb.uow import MongoDBContext, MongoDBUnitOfWork
from fastapi import Depends

from app.core.config import Settings
from app.dependencies.settings import get_settings


@lru_cache(maxsize=1)
def get_mongo_context(
    settings: Annotated[Settings, Depends(get_settings)],
) -> MongoDBContext:
    return MongoDBContext.from_settings(
        host=settings.mongo_uri,
        database_name=settings.mongo_database,
    )


def get_mongo_uow(
    context: Annotated[MongoDBContext, Depends(get_mongo_context)],
) -> MongoDBUnitOfWork:
    return MongoDBUnitOfWork(context=context)
