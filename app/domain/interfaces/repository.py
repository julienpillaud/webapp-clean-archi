from typing import Protocol

from app.domain.entities import DomainEntity, EntityId, PaginatedResponse, Pagination
from app.domain.filters import FilterEntity


class RepositoryProtocol[T: DomainEntity](Protocol):
    def get_all(
        self,
        pagination: Pagination | None = None,
        search: str | None = None,
        filters: list[FilterEntity] | None = None,
    ) -> PaginatedResponse[T]: ...

    def get_by_id(self, entity_id: EntityId, /) -> T | None: ...

    def create(self, entity: T, /) -> T: ...

    def update(self, entity: T, /) -> T: ...

    def delete(self, entity: T, /) -> None: ...
