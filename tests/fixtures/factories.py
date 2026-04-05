import pytest
from cleanstack.infrastructure.sql.uow import SQLContext

from tests.factories.posts import PostSQLFactory
from tests.factories.users import UserSQLFactory


@pytest.fixture
def user_factory(sql_context: SQLContext) -> UserSQLFactory:
    return UserSQLFactory(context=sql_context)


@pytest.fixture
def post_factory(sql_context: SQLContext) -> PostSQLFactory:
    return PostSQLFactory(context=sql_context)
