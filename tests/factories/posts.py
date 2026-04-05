import uuid
from typing import Any

from cleanstack.factories.sql import BaseSQLFactory

from app.domain.posts.entities import Post
from app.infrastructure.sql.posts import PostSQLRepository
from tests.factories.users import UserSQLFactory


def generate_post(**kwargs: Any) -> Post:
    return Post(
        id=uuid.uuid7(),
        title=kwargs.get("title", "Post Title"),
        content=kwargs.get("content", "post content"),
        author_id=kwargs["author_id"],
        tags=[],
    )


class PostSQLFactory(BaseSQLFactory[Post]):
    @property
    def user_factory(self) -> UserSQLFactory:
        return UserSQLFactory(context=self.context)

    def build(self, **kwargs: Any) -> Post:
        if "author_id" not in kwargs:
            kwargs["author_id"] = self.user_factory.create_one().id
        return generate_post(**kwargs)

    @property
    def _repository(self) -> PostSQLRepository:
        return PostSQLRepository(session=self.uow.session)
