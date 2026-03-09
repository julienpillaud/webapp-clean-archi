from cleanstack.entities import FilterEntity, PaginatedResponse, Pagination, SortEntity

from app.domain.context import ContextProtocol
from app.domain.users.entities import User


def get_user_by_provider_id_command(
    context: ContextProtocol,
    /,
    provider_id: str,
) -> User | None:
    return context.user_repository.get_by_provider_id(provider_id)


def get_users_command(
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
