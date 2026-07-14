import pytest

from app.infrastructure.sql.resource import SQLResource
from tests.factories.posts import PostSQLFactory
from tests.factories.users import UserSQLFactory


class Factory:
    def __init__(self, users: UserSQLFactory, posts: PostSQLFactory) -> None:
        self.users = users
        self.posts = posts


@pytest.fixture
def factory(db_resource: SQLResource) -> Factory:
    return Factory(
        users=UserSQLFactory(db_resource.session_factory),
        posts=PostSQLFactory(db_resource.session_factory),
    )
