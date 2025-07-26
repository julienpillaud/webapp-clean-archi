from typing import ClassVar

from polyfactory.factories.pydantic_factory import ModelFactory

from app.domain.posts.entities import Post
from app.domain.users.entities import User


class PostFactory(ModelFactory[Post]):
    # Create between 1 and 3 tags
    __randomize_collection_length__ = True
    __min_collection_length__ = 1
    __max_collection_length__ = 3


class UserFactory(ModelFactory[User]):
    posts: ClassVar[list[Post]] = []
