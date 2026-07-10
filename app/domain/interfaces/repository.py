from typing import Protocol

from cleanstack import (
    BaseEntity,
    EntityId,
    FilterEntity,
    PaginatedResponse,
    Pagination,
    SortEntity,
)


class RepositoryProtocol[T: BaseEntity](Protocol):
    def get_all(
        self,
        search: str | None = None,
        filters: list[FilterEntity] | None = None,
        sort: list[SortEntity] | None = None,
        pagination: Pagination | None = None,
    ) -> PaginatedResponse[T]: ...

    def get_by_id(self, entity_id: EntityId, /) -> T | None: ...

    def save(self, entity: T, /) -> None: ...

    def update(self, entity: T, /) -> None: ...

    def remove(self, entity: T, /) -> None: ...
