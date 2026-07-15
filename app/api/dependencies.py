from collections.abc import Callable, Iterator
from functools import lru_cache
from typing import Annotated

from cleanstack.entities import FilterEntity, SortEntity
from fastapi import Depends, HTTPException, Query, status
from starlette.requests import Request

from app.api.utils import parse_filters
from app.core.config import Settings
from app.core.context import ContextProvider
from app.core.domain.synchronous import Domain, DomainContext, TransactionProtocol
from app.domain.context import ContextProtocol
from app.infrastructure.sql.resource import SQLTransaction


@lru_cache
def get_settings() -> Settings:
    return Settings()


def get_sql_transaction(request: Request) -> SQLTransaction:
    sql_engine = request.app.state.sql_resource
    return SQLTransaction(sql_engine)


def get_context_provider(
    settings: Annotated[Settings, Depends(get_settings)],
) -> Callable[[TransactionProtocol], ContextProtocol]:
    return ContextProvider(settings=settings)


def get_domain(
    sql_resource: Annotated[SQLTransaction, Depends(get_sql_transaction)],
    context_provider: Annotated[
        Callable[[TransactionProtocol], ContextProtocol],
        Depends(get_context_provider),
    ],
) -> Iterator[Domain]:
    with DomainContext(
        transaction=sql_resource,
        context_provider=context_provider,
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
