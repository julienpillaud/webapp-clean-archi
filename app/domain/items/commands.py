import uuid

import logfire
from cleanstack.entities import FilterEntity, PaginatedResponse, Pagination, SortEntity

from app.domain.context import ContextProtocol
from app.domain.interfaces.event_publisher import Event
from app.domain.items.entities import Item, ItemMessage
from app.domain.items.repository import RepositoryType


def get_items_command(
    context: ContextProtocol,
    /,
    repository: RepositoryType,
    search: str | None = None,
    filters: list[FilterEntity] | None = None,
    sort: list[SortEntity] | None = None,
    pagination: Pagination | None = None,
) -> PaginatedResponse[Item]:
    match repository:
        case RepositoryType.RELATIONAL:
            return context.item_relational_repository.get_all(
                search=search,
                filters=filters,
                sort=sort,
                pagination=pagination,
            )
        case RepositoryType.DOCUMENT:
            return context.item_document_repository.get_all(
                search=search,
                filters=filters,
                sort=sort,
                pagination=pagination,
            )


def send_item_event_command(context: ContextProtocol, /) -> None:
    context.event_publisher.publish(
        events=[
            Event(
                queue="item.event",
                message=ItemMessage(
                    item_id=uuid.uuid7(),
                    message="Hello world!",
                ),
            ),
            Event(
                queue="item.event",
                message=ItemMessage(
                    item_id=uuid.uuid7(),
                    message="Goodbye world!",
                ),
            ),
        ]
    )


def handle_item_event_command(
    context: ContextProtocol,
    /,
    message: ItemMessage,
) -> None:
    logfire.info(f"Processing event: {message}")
