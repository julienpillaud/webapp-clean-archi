from app.domain.context import ContextProtocol
from app.domain.entities import PaginatedResponse, Pagination
from app.domain.filters import FilterEntity
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
    pagination: Pagination | None = None,
    search: str | None = None,
    filters: list[FilterEntity] | None = None,
) -> PaginatedResponse[User]:
    return context.user_repository.get_all(
        pagination=pagination,
        search=search,
        filters=filters,
    )
