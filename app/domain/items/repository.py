from typing import Protocol

from cleanstack import FilterEntity, PaginatedResponse, Pagination, SortEntity

from app.domain.items.entities import Item


class ItemRepositoryProtocol(Protocol):
    def get_all(
        self,
        search: str | None = None,
        filters: list[FilterEntity] | None = None,
        sort: list[SortEntity] | None = None,
        pagination: Pagination | None = None,
    ) -> PaginatedResponse[Item]: ...

    def save(self, entity: Item, /) -> None: ...
