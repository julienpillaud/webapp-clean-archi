from collections.abc import Callable, Iterator
from functools import lru_cache
from typing import Annotated

from cleanstack.entities import FilterEntity, SortEntity
from fastapi import Depends, HTTPException, Query, status
from starlette.requests import Request

from app.api.utils import parse_filters
from app.core.config import Settings
from app.core.context import ContextProvider
from app.core.domain.synchronous import Domain, DomainManager, ResourceProtocol
from app.domain.context import ContextProtocol
from app.infrastructure.sql.resource import SQLResource


@lru_cache
def get_settings() -> Settings:
    return Settings()


def get_sql_resource(request: Request) -> SQLResource:
    sql_engine = request.app.state.sql_engine
    return SQLResource(sql_engine)


def get_context_provider(
    settings: Annotated[Settings, Depends(get_settings)],
) -> Callable[[ResourceProtocol], ContextProtocol]:
    return ContextProvider(settings=settings)


class DomainProvider:
    def __init__(
        self,
        transactional: bool = False,
        scope: str = "domain",
    ) -> None:
        self._transactional = transactional
        self._scope = scope

    def __call__(
        self,
        request: Request,
        sql_resource: Annotated[SQLResource, Depends(get_sql_resource)],
        context_provider: Annotated[
            Callable[[ResourceProtocol], ContextProtocol],
            Depends(get_context_provider),
        ],
    ) -> Iterator[Domain]:
        if not hasattr(request.state, "domains_cache"):
            request.state.domains_cache = {}

        existing_domain = request.state.domains_cache.get(self._scope)
        if existing_domain is not None:
            yield existing_domain
            return

        with DomainManager(
            resource=sql_resource,
            context_provider=context_provider,
            transactional=self._transactional,
        ) as domain:
            request.state.domains_cache[self._scope] = domain

            try:
                yield domain
            finally:
                request.state.domains_cache.pop(self._scope, None)


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
