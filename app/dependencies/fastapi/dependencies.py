from collections.abc import Iterator
from typing import Annotated

from cleanstack.entities import FilterEntity, SortEntity
from fastapi import Depends, HTTPException, Query, status
from fastapi.security import HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from starlette.requests import Request

from app.api.security import decode_jwt, http_bearer
from app.api.utils import parse_filters
from app.core.config import Settings
from app.core.context import Context
from app.dependencies.settings import get_settings
from app.domain.users.commands import get_user_by_provider_id_command
from app.domain.users.entities import User
from app.infrastructure.sql.utils import managed_session

credential_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials.",
)


def get_session(request: Request) -> Iterator[Session]:
    with managed_session(request.app.state.sql_session_factory) as session:
        yield session


def get_context(
    settings: Annotated[Settings, Depends(get_settings)],
    session: Annotated[Session, Depends(get_session)],
) -> Context:
    return Context(settings=settings, session=session)


async def get_current_user(
    settings: Annotated[Settings, Depends(get_settings)],
    context: Annotated[Context, Depends(get_context)],
    credentials: Annotated[HTTPAuthorizationCredentials | None, Depends(http_bearer)],
) -> User:
    if not credentials:
        raise credential_exception

    payload = decode_jwt(credentials.credentials, settings=settings)
    if not payload:
        raise credential_exception

    user = get_user_by_provider_id_command(context, provider_id=payload.sub)
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


def get_sort_entities() -> list[SortEntity]:
    return []
