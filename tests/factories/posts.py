import uuid
from typing import Any

from cleanstack.factories.sql import BaseSQLFactory

from app.domain.posts.entities import Post
from app.infrastructure.sql.posts import PostSQLRepository
from tests.factories.faker import faker
from tests.factories.users import UserSQLFactory


def generate_post(**kwargs: Any) -> Post:
    return Post(
        id=uuid.uuid7(),
        title=kwargs.get("title", faker.random_string()),
        content=kwargs.get("content", faker.random_string()),
        author_id=kwargs["author_id"],
        tags=kwargs.get(
            "tags",
            [
                faker.random_string(string_length=20)
                for _ in range(faker.random_int(min_value=1, max_value=3))
            ],
        ),
    )


class PostSQLFactory(BaseSQLFactory[Post]):
    @property
    def user_factory(self) -> UserSQLFactory:
        return UserSQLFactory(session_factory=self.session_factory)

    def build(self, **kwargs: Any) -> Post:
        if "author_id" not in kwargs:
            kwargs["author_id"] = self.user_factory.create_one().id
        return generate_post(**kwargs)

    @property
    def _repository(self) -> PostSQLRepository:
        return PostSQLRepository(session=self.session)
