from cleanstack.entities import FilterEntity, PaginatedResponse, Pagination, SortEntity

from app.domain.context import ContextProtocol
from app.domain.users.entities import User


def get_users(
    context: ContextProtocol,
    /,
    search: str | None = None,
    filters: list[FilterEntity] | None = None,
    sort: list[SortEntity] | None = None,
    pagination: Pagination | None = None,
) -> PaginatedResponse[User]:
    return context.user_repository.get_all(
        search=search,
        filters=filters,
        sort=sort,
        pagination=pagination,
    )
