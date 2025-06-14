from typing import Protocol, TypeVar

from app.domain.entities import DomainModel, EntityId, PaginatedResponse, Pagination

T = TypeVar("T", bound=DomainModel)


class BaseRepositoryProtocol(Protocol[T]):
    def get_all(
        self,
        pagination: Pagination | None = None,
        search: str | None = None,
    ) -> PaginatedResponse[T]: ...
    def get_by_id(self, entity_id: EntityId, /) -> T | None: ...
    def create(self, entity: T, /) -> T: ...
    def update(self, entity: T, /) -> T: ...
    def delete(self, entity: T, /) -> None: ...
