from sqlalchemy import select

from app.domain.entities import TagName
from app.domain.exceptions import NotFoundError
from app.domain.posts.entities import Post
from app.domain.posts.repository import PostRepositoryProtocol
from app.infrastructure.repository.base import BaseSqlRepository
from app.infrastructure.repository.models import OrmPost, OrmTag


class PostSqlRepository(
    BaseSqlRepository[Post, OrmPost],
    PostRepositoryProtocol,
):
    domain_model = Post
    orm_model = OrmPost

    def update(self, entity: Post, /) -> Post:
        orm_entity = self._get_entity_by_id(entity_id=entity.id)
        if not orm_entity:
            raise NotFoundError(f"Post '{entity.id}' not found.")

        for key, value in entity.model_dump(exclude={"id", "tags"}).items():
            if hasattr(orm_entity, key):
                setattr(orm_entity, key, value)

        self._update_tags(entity=entity, orm_entity=orm_entity)
        return self.orm_to_domain_entity(orm_entity=orm_entity)

    def _update_tags(self, entity: Post, orm_entity: OrmPost) -> None:
        orm_entity.tags.clear()

        for tag_name in entity.tags:
            stmt = select(OrmTag).where(OrmTag.name == tag_name)
            orm_tag = self.session.scalar(stmt)
            if not orm_tag:
                orm_tag = OrmTag(name=tag_name)
                self.session.add(orm_tag)

            orm_entity.tags.append(orm_tag)

    def domain_to_orm_entity(self, entity: Post) -> OrmPost:
        return OrmPost(
            id=entity.id,
            title=entity.title,
            content=entity.content,
            author_id=entity.author_id,
            tags=[OrmTag(name=tag) for tag in entity.tags],
        )

    def orm_to_domain_entity(self, orm_entity: OrmPost) -> Post:
        return Post(
            id=orm_entity.id,
            title=orm_entity.title,
            content=orm_entity.content,
            author_id=orm_entity.author_id,
            tags=[TagName(tag.name) for tag in orm_entity.tags],
        )
