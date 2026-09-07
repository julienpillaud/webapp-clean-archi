from typing import Protocol

from cleanstack import (
    EntityId,
    FilterEntity,
    PaginatedResponse,
    Pagination,
    SortEntity,
)

from app.domain.posts.entities import Post


class PostRepositoryProtocol(Protocol):
    def get_all(
        self,
        search: str | None = None,
        filters: list[FilterEntity] | None = None,
        sort: list[SortEntity] | None = None,
        pagination: Pagination | None = None,
    ) -> PaginatedResponse[Post]: ...

    def get_by_id(self, entity_id: EntityId, /) -> Post | None: ...

    def save(self, entity: Post, /) -> None: ...

    def update(self, entity: Post, /) -> None: ...

    def remove(self, entity: Post, /) -> None: ...
