from collections.abc import Iterator
from functools import lru_cache
from typing import Annotated

from cleanstack.entities import FilterEntity, SortEntity
from fastapi import Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from starlette.requests import Request

from app.api.utils import parse_filters
from app.core.config import Settings
from app.core.context import Context, ContextFactory
from app.core.domain import Domain


@lru_cache
def get_settings() -> Settings:
    return Settings()


def get_context_factory(
    settings: Annotated[Settings, Depends(get_settings)],
) -> ContextFactory:

    def _get_context(session: Session) -> Context:
        return Context(settings=settings, session=session)

    return _get_context


def get_domain(
    request: Request,
    context_factory: Annotated[ContextFactory, Depends(get_context_factory)],
) -> Iterator[Domain]:
    sql_resource = request.app.state.sql_resource
    with Domain(
        resource=sql_resource,
        context_factory=context_factory,
    ) as domain:
        yield domain


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
