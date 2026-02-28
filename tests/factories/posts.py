import uuid
from typing import Any

from faker import Faker

from app.domain.posts.entities import Post
from app.infrastructure.sql.repositories.posts import PostSQLRepository
from tests.factories.base import BaseSQLFactory
from tests.factories.users import UserSQLFactory


def generate_post(faker: Faker, **kwargs: Any) -> Post:
    return Post(
        id=uuid.uuid7(),
        title=kwargs["title"] if "title" in kwargs else faker.sentence(),
        content=kwargs["content"] if "content" in kwargs else faker.text(),
        author_id=kwargs["author_id"],
        tags=[],
    )


class PostSQLFactory(BaseSQLFactory[Post]):
    @property
    def user_factory(self) -> UserSQLFactory:
        return UserSQLFactory(faker=self.faker, context=self.context)

    def build(self, **kwargs: Any) -> Post:
        if "author_id" not in kwargs:
            kwargs["author_id"] = self.user_factory.create_one().id
        return generate_post(faker=self.faker, **kwargs)

    @property
    def _repository(self) -> PostSQLRepository:
        return PostSQLRepository(session=self.uow.session)
