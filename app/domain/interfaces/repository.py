import uuid
from typing import Protocol, TypeVar

from app.domain.entities import DomainModel, PaginatedResponse, Pagination

T = TypeVar("T", bound=DomainModel)


class BaseRepositoryProtocol(Protocol[T]):
    def get_all(self, pagination: Pagination | None = None) -> PaginatedResponse[T]: ...
    def get_by_id(self, entity_id: uuid.UUID, /) -> T | None: ...
    def create(self, entity: T, /) -> None: ...
    def update(self, entity: T, /) -> None: ...
    def delete(self, entity_id: uuid.UUID, /) -> None: ...
