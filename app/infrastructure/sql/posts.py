import uuid

from cleanstack import EntityId, FilterEntity, PaginatedResponse, Pagination, SortEntity
from cleanstack.sql import SyncSQLRepository
from sqlalchemy.orm import Session

from app.domain.posts.entities import Post, TagName
from app.domain.posts.repository import PostRepositoryProtocol
from app.infrastructure.sql.models import OrmPost, OrmTag


class PostSQLAdapter(SyncSQLRepository[Post, OrmPost]):
    def to_domain_entity(self, orm_entity: OrmPost, /) -> Post:
        return Post(
            id=orm_entity.id,
            title=orm_entity.title,
            content=orm_entity.content,
            author_id=orm_entity.author_id,
            tags=[TagName(tag.name) for tag in orm_entity.tags],
        )

    def to_database_entity(self, entity: Post) -> OrmPost:
        return OrmPost(
            id=entity.id,
            title=entity.title,
            content=entity.content,
            author_id=entity.author_id,
            tags=[OrmTag(id=uuid.uuid7(), name=tag) for tag in entity.tags],
        )


class PostSQLRepository(PostRepositoryProtocol):
    domain_entity_type = Post
    orm_model_type = OrmPost
    searchable_fields = ("title", "content")

    def __init__(self, session: Session) -> None:
        self.session = session
        self.repository = PostSQLAdapter.from_binding(
            binding=self,
            session=session,
        )

    def get_all(
        self,
        search: str | None = None,
        filters: list[FilterEntity] | None = None,
        sort: list[SortEntity] | None = None,
        pagination: Pagination | None = None,
    ) -> PaginatedResponse[Post]:
        return self.repository.get_all(
            search=search,
            filters=filters,
            sort=sort,
            pagination=pagination,
        )

    def get_by_id(self, entity_id: EntityId, /) -> Post | None:
        return self.repository.get_by_id(entity_id)

    def save(self, entity: Post, /) -> None:
        self.repository.save(entity)

    def update(self, entity: Post, /) -> None:
        self.repository.update(entity)

    def remove(self, entity: Post, /) -> None:
        self.repository.remove(entity)
