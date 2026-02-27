from typing import Annotated

from fast_depends import Depends

from app.core.config import Settings
from app.core.context import Context
from app.core.uow import UnitOfWork
from app.dependencies.faststream.mongo import get_mongo_uow
from app.dependencies.faststream.sql import get_sql_uow
from app.dependencies.settings import get_settings
from app.domain.domain import Domain
from app.infrastructure.mongo.uow import MongoUnitOfWork
from app.infrastructure.sql.uow import SQLUnitOfWork


def get_uow(
    sql_uow: Annotated[SQLUnitOfWork, Depends(get_sql_uow)],
    mongo_uow: Annotated[MongoUnitOfWork, Depends(get_mongo_uow)],
) -> UnitOfWork:
    return UnitOfWork(sql=sql_uow, mongo=mongo_uow)


def get_context(
    settings: Annotated[Settings, Depends(get_settings)],
    uow: Annotated[UnitOfWork, Depends(get_uow)],
) -> Context:
    return Context(settings=settings, uow=uow)


def get_domain(
    uow: Annotated[UnitOfWork, Depends(get_uow)],
    context: Annotated[Context, Depends(get_context)],
) -> Domain:
    return Domain(uow=uow, context=context)
