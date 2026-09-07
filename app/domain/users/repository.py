from typing import Protocol

from cleanstack import (
    EntityId,
    FilterEntity,
    PaginatedResponse,
    Pagination,
    SortEntity,
)

from app.domain.users.entities import User


class UserRepositoryProtocol(Protocol):
    def get_all(
        self,
        search: str | None = None,
        filters: list[FilterEntity] | None = None,
        sort: list[SortEntity] | None = None,
        pagination: Pagination | None = None,
    ) -> PaginatedResponse[User]: ...

    def get_by_id(self, entity_id: EntityId, /) -> User | None: ...

    def save(self, entity: User, /) -> None: ...
