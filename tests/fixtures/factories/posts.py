from typing import Any

from sqlalchemy.orm import Session

from app.domain.posts.entities import Post, TagName
from app.infrastructure.sql.models import OrmPost, OrmTag
from tests.fixtures.factories.sql import SqlBaseFactory
from tests.fixtures.factories.users import UserSqlFactory


class PostSqlFactory(SqlBaseFactory[Post, OrmPost]):
    def __init__(self, session: Session, user_factory: UserSqlFactory):
        super().__init__(session)
        self.user_factory = user_factory

    def _build_entity(self, **kwargs: Any) -> Post:
        if not (author_id := kwargs.get("author_id")):
            author_id = self.user_factory.create_one().id

        if not (tags := kwargs.get("tags")):
            num_tags = self.faker.random_int(min=1, max=3)
            tags = [
                TagName(f"{self.faker.unique.lexify(text='?????')}{i}")
                for i in range(num_tags)
            ]

        return Post(
            id=None,
            title=kwargs.get("title", self.faker.sentence()),
            content=kwargs.get("content", self.faker.text()),
            author_id=author_id,
            tags=tags,
        )

    def _to_database_entity(self, entity: Post) -> OrmPost:
        return OrmPost(
            id=entity.id,
            title=entity.title,
            content=entity.content,
            author_id=entity.author_id,
            tags=[OrmTag(name=tag) for tag in entity.tags],
        )
