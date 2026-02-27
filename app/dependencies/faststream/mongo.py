from functools import lru_cache
from typing import Annotated

from fast_depends import Depends

from app.core.config import Settings
from app.dependencies.settings import get_settings
from app.infrastructure.mongo.uow import MongoContext, MongoUnitOfWork


@lru_cache(maxsize=1)
def get_mongo_context(
    settings: Annotated[Settings, Depends(get_settings)],
) -> MongoContext:
    return MongoContext.from_settings(
        uri=settings.mongo_uri,
        database_name=settings.mongo_database,
    )


def get_mongo_uow(
    context: Annotated[MongoContext, Depends(get_mongo_context)],
) -> MongoUnitOfWork:
    return MongoUnitOfWork(context=context)
