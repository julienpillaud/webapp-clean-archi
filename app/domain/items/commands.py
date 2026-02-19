from app.domain.context import ContextProtocol
from app.domain.entities import PaginatedResponse, Pagination
from app.domain.filters import FilterEntity
from app.domain.items.entities import Item
from app.domain.items.repository import RepositoryType


def get_items_command(
    context: ContextProtocol,
    /,
    repository: RepositoryType,
    pagination: Pagination | None = None,
    search: str | None = None,
    filters: list[FilterEntity] | None = None,
) -> PaginatedResponse[Item]:
    match repository:
        case RepositoryType.RELATIONAL:
            return context.item_relational_repository.get_all(
                pagination=pagination,
                search=search,
                filters=filters,
            )
        case RepositoryType.DOCUMENT:
            return context.item_document_repository.get_all(
                pagination=pagination,
                search=search,
                filters=filters,
            )
