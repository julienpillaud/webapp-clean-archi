from functools import lru_cache
from typing import Annotated, cast

from fastapi import Depends, HTTPException, Query, status
from fastapi.security import HTTPAuthorizationCredentials
from starlette.requests import Request

from app.api.security import decode_jwt, http_bearer
from app.api.utils import parse_filters
from app.core.config import Settings
from app.domain.domain import Domain
from app.domain.filters import FilterEntity
from app.domain.users.entities import User

credential_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials.",
)


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings()  # ty:ignore[missing-argument]


def get_domain(request: Request) -> Domain:
    return cast(Domain, request.app.state.domain)


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
