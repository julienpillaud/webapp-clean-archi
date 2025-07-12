import uuid
from typing import Any, TypeVar

from app.domain.posts.entities import Post, TagName
from tests.fixtures.factories.base import BaseFactory, faker
from tests.fixtures.factories.users.base import UserBaseFactory

P = TypeVar("P")


class PostBaseFactory(BaseFactory[Post]):
    def __init__(self, user_factory: UserBaseFactory) -> None:
        self.user_factory = user_factory

    def _build_entity(self, **kwargs: Any) -> Post:
        if not (author_id := kwargs.get("author_id")):
            author_id = self.user_factory.create_one().id

        if not (tags := kwargs.get("tags")):
            num_tags = faker.random_int(min=1, max=3)
            tags = [
                TagName(f"{faker.unique.lexify(text='?????')}{i}")
                for i in range(num_tags)
            ]

        return Post(
            id=uuid.uuid4(),
            title=kwargs.get("title", faker.sentence()),
            content=kwargs.get("content", faker.text()),
            author_id=author_id,
            tags=tags,
        )
