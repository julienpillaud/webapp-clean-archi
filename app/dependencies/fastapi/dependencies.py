from typing import Annotated

from cleanstack.infrastructure.mongodb.uow import MongoDBContext, MongoDBUnitOfWork
from cleanstack.infrastructure.sql.uow import SQLUnitOfWork
from fastapi import Depends, HTTPException, Query, status
from fastapi.security import HTTPAuthorizationCredentials

from app.api.security import decode_jwt, http_bearer
from app.api.utils import parse_filters
from app.core.config import Settings
from app.core.context import Context
from app.core.uow import UnitOfWork
from app.dependencies.fastapi.mongo import get_mongo_context, get_mongo_uow
from app.dependencies.fastapi.sql import get_sql_uow
from app.dependencies.settings import get_settings
from app.domain.domain import Domain
from app.domain.filters import FilterEntity
from app.domain.users.entities import User

credential_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials.",
)


def get_uow(
    sql_uow: Annotated[SQLUnitOfWork, Depends(get_sql_uow)],
    mongo_uow: Annotated[MongoDBUnitOfWork, Depends(get_mongo_uow)],
) -> UnitOfWork:
    return UnitOfWork(sql=sql_uow, mongo=mongo_uow)


def get_context(
    settings: Annotated[Settings, Depends(get_settings)],
    sql_uow: Annotated[SQLUnitOfWork, Depends(get_sql_uow)],
    mongo_context: Annotated[MongoDBContext, Depends(get_mongo_context)],
    mongo_uow: Annotated[MongoDBUnitOfWork, Depends(get_mongo_uow)],
) -> Context:
    return Context(
        settings=settings,
        sql_uow=sql_uow,
        mongo_context=mongo_context,
        mongo_uow=mongo_uow,
    )


def get_domain(
    uow: Annotated[UnitOfWork, Depends(get_uow)],
    context: Annotated[Context, Depends(get_context)],
) -> Domain:
    return Domain(uow=uow, context=context)


async def get_current_user(
    settings: Annotated[Settings, Depends(get_settings)],
    domain: Annotated[Domain, Depends(get_domain)],
    credentials: Annotated[HTTPAuthorizationCredentials | None, Depends(http_bearer)],
) -> User:
    if not credentials:
        raise credential_exception

    payload = decode_jwt(credentials.credentials, settings=settings)
    if not payload:
        raise credential_exception

    user = domain.get_user_by_provider_id(provider_id=payload.sub)
    if user is None:
        raise credential_exception

    return user


def get_filters(
    filters: Annotated[list[str] | None, Query(alias="filter")] = None,
) -> list[FilterEntity]:
    if not filters:
        return []

    try:
        return parse_filters(filters)
    except ValueError as error:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Invalid filter format.",
        ) from error
