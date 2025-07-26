from typing import Any

from app.domain.posts.entities import Post
from factories.base import BaseFactory
from factories.factories import PostFactory
from factories.users.base import UserBaseFactory


class PostBaseFactory(BaseFactory[Post]):
    def __init__(self, user_factory: UserBaseFactory) -> None:
        self.user_factory = user_factory

    def _build_entity(self, **kwargs: Any) -> Post:
        if "author_id" not in kwargs:
            kwargs["author_id"] = self.user_factory.create_one().id
        return PostFactory.build(**kwargs)
