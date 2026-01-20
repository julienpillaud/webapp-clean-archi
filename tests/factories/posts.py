import uuid
from typing import Any

from faker import Faker

from app.domain.posts.entities import Post
from app.infrastructure.sql.models import OrmPost
from app.infrastructure.sql.posts import PostSqlRepository
from tests.factories.base import BaseSqlFactory
from tests.factories.users import UserFactory


def generate_post(faker: Faker, **kwargs: Any) -> Post:
    return Post(
        id=uuid.uuid7(),
        title=kwargs["title"] if "title" in kwargs else faker.sentence(),
        content=kwargs["content"] if "content" in kwargs else faker.text(),
        author_id=kwargs["author_id"],
        tags=[],
    )


class PostFactory(BaseSqlFactory[Post, OrmPost]):
    repository_class = PostSqlRepository

    @property
    def user_factory(self) -> UserFactory:
        return UserFactory(faker=self.faker, session=self.session)

    def build(self, **kwargs: Any) -> Post:
        if "author_id" not in kwargs:
            kwargs["author_id"] = self.user_factory.create_one().id
        return generate_post(faker=self.faker, **kwargs)
