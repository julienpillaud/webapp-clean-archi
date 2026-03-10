import pytest
from cleanstack.infrastructure.sql.uow import SQLContext
from faker import Faker

from tests.factories.posts import PostSQLFactory
from tests.factories.users import UserSQLFactory


@pytest.fixture
def faker() -> Faker:
    return Faker()


@pytest.fixture
def user_factory(faker: Faker, sql_context: SQLContext) -> UserSQLFactory:
    return UserSQLFactory(faker=faker, context=sql_context)


@pytest.fixture
def post_factory(faker: Faker, sql_context: SQLContext) -> PostSQLFactory:
    return PostSQLFactory(faker=faker, context=sql_context)
