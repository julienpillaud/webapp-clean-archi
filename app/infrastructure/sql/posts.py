import uuid

from sqlalchemy import select
from sqlalchemy.orm import selectinload

from app.domain.posts.entities import Post, TagName
from app.domain.posts.repository import PostRepositoryProtocol
from app.infrastructure.sql.base import SqlRepository
from app.infrastructure.sql.models import OrmPost, OrmTag


class PostSqlRepository(SqlRepository[Post, OrmPost], PostRepositoryProtocol):
    domain_model = Post
    orm_model = OrmPost
    select_options = (selectinload(OrmPost.tags),)
    searchable_fields = (OrmPost.title, OrmPost.content)

    def update(self, entity: Post, /) -> Post:
        assert entity.id is not None

        db_entity = self._get_db_entity(entity_id=entity.id)
        if not db_entity:
            raise RuntimeError()

        for key, value in entity.model_dump(exclude={"id", "tags"}).items():
            if hasattr(db_entity, key):
                setattr(db_entity, key, value)
        self._update_tags(entity=entity, orm_entity=db_entity)

        return self._to_domain_entity(db_entity)

    def _update_tags(self, entity: Post, orm_entity: OrmPost) -> None:
        orm_entity.tags.clear()

        for tag_name in entity.tags:
            stmt = select(OrmTag).where(OrmTag.name == tag_name)
            orm_tag = self.session.scalar(stmt)
            if not orm_tag:
                orm_tag = OrmTag(id=uuid.uuid4(), name=tag_name)
                self.session.add(orm_tag)

            orm_entity.tags.append(orm_tag)

    def _to_database_entity(self, entity: Post, /) -> OrmPost:
        return OrmPost(
            id=entity.id,
            title=entity.title,
            content=entity.content,
            author_id=entity.author_id,
            tags=[OrmTag(id=uuid.uuid4(), name=tag) for tag in entity.tags],
        )

    def _to_domain_entity(self, orm_entity: OrmPost, /) -> Post:
        return Post(
            id=orm_entity.id,
            title=orm_entity.title,
            content=orm_entity.content,
            author_id=orm_entity.author_id,
            tags=[TagName(tag.name) for tag in orm_entity.tags],
        )
