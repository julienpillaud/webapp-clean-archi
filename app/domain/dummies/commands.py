from app.domain.caching import cached_command
from app.domain.context import ContextProtocol
from app.domain.dummies.entities import Dummy
from app.domain.entities import PaginatedResponse, Pagination
from app.domain.filters import FilterEntity


@cached_command(response_model=PaginatedResponse[Dummy], tag="dummies")
def get_dummies_command(
    context: ContextProtocol,
    /,
    pagination: Pagination | None = None,
    search: str | None = None,
    filters: list[FilterEntity] | None = None,
) -> PaginatedResponse[Dummy]:
    return context.dummy_repository.get_all(
        pagination=pagination,
        search=search,
        filters=filters,
    )
