import uuid
from typing import Any

from cleanstack.factories.sql import SqlBaseFactory
from polyfactory.factories.pydantic_factory import ModelFactory
from sqlalchemy.orm import Session

from app.domain.posts.entities import Post
from app.infrastructure.sql.models import OrmPost, OrmTag
from factories.users import UserFactory


class PostEntityFactory(ModelFactory[Post]):
    __check_model__ = True
    # Create between 1 and 3 tags
    __randomize_collection_length__ = True
    __min_collection_length__ = 1
    __max_collection_length__ = 3


class PostFactory(SqlBaseFactory[Post, OrmPost]):
    orm_model = OrmPost

    def __init__(self, session: Session) -> None:
        super().__init__(session=session)

    @property
    def user_factory(self) -> UserFactory:
        return UserFactory(session=self.session)

    def _build_entity(self, **kwargs: Any) -> Post:
        if "author_id" not in kwargs:
            kwargs["author_id"] = self.user_factory.create_one().id
        return PostEntityFactory.build(**kwargs)

    def _to_database_entity(self, entity: Post) -> OrmPost:
        return OrmPost(
            id=entity.id,
            title=entity.title,
            content=entity.content,
            author_id=entity.author_id,
            tags=[OrmTag(id=uuid.uuid4(), name=tag) for tag in entity.tags],
        )
