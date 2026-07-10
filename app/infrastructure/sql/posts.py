import uuid

from cleanstack.sql import SyncSQLRepository

from app.domain.posts.entities import Post, TagName
from app.infrastructure.sql.models import OrmPost, OrmTag


class PostSQLRepository(SyncSQLRepository[Post, OrmPost]):
    domain_entity_type = Post
    orm_model_type = OrmPost
    searchable_fields = ("title", "content")

    def to_orm_entity(self, entity: Post) -> OrmPost:
        return OrmPost(
            id=entity.id,
            title=entity.title,
            content=entity.content,
            author_id=entity.author_id,
            tags=[OrmTag(id=uuid.uuid7(), name=tag) for tag in entity.tags],
        )

    def to_domain_entity(self, orm_entity: OrmPost, /) -> Post:
        return Post(
            id=orm_entity.id,
            title=orm_entity.title,
            content=orm_entity.content,
            author_id=orm_entity.author_id,
            tags=[TagName(tag.name) for tag in orm_entity.tags],
        )
