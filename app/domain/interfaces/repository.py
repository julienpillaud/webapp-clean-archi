from typing import Protocol

from cleanstack.entities import DomainModel, EntityId

from app.domain.entities import PaginatedResponse, Pagination


class BaseRepositoryProtocol[T: DomainModel](Protocol):
    def get_all(
        self,
        pagination: Pagination | None = None,
        search: str | None = None,
    ) -> PaginatedResponse[T]: ...
    def get_by_id(self, entity_id: EntityId, /) -> T | None: ...
    def create(self, entity: T, /) -> T: ...
    def update(self, entity: T, /) -> T: ...
    def delete(self, entity: T, /) -> None: ...
