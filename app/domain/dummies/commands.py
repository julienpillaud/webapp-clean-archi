from cleanstack.entities import FilterEntity, PaginatedResponse, Pagination, SortEntity

from app.domain.caching import cached_command
from app.domain.context import ContextProtocol
from app.domain.dummies.entities import Dummy


def get_dummies_command(
    context: ContextProtocol,
    /,
    search: str | None = None,
    filters: list[FilterEntity] | None = None,
    sort: list[SortEntity] | None = None,
    pagination: Pagination | None = None,
) -> PaginatedResponse[Dummy]:
    return context.dummy_repository.get_all(
        search=search,
        filters=filters,
        sort=sort,
        pagination=pagination,
    )


@cached_command(response_model=PaginatedResponse[Dummy], tag="dummies")
def get_dummies_cached_command(
    context: ContextProtocol,
    /,
    search: str | None = None,
    filters: list[FilterEntity] | None = None,
    sort: list[SortEntity] | None = None,
    pagination: Pagination | None = None,
) -> PaginatedResponse[Dummy]:
    return context.dummy_repository.get_all(
        search=search,
        filters=filters,
        sort=sort,
        pagination=pagination,
    )
