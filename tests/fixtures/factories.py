import pytest
from cleanstack.infrastructure.mongodb.uow import MongoDBContext
from cleanstack.infrastructure.sql.uow import SQLContext
from faker import Faker

from tests.factories.dummies import DummySQLFactory
from tests.factories.items import ItemMongoFactory, ItemSQLFactory
from tests.factories.posts import PostSQLFactory
from tests.factories.users import UserSQLFactory


@pytest.fixture
def faker() -> Faker:
    return Faker()


@pytest.fixture
def dummy_factory(faker: Faker, sql_context: SQLContext) -> DummySQLFactory:
    return DummySQLFactory(faker=faker, context=sql_context)


@pytest.fixture
def item_sql_factory(faker: Faker, sql_context: SQLContext) -> ItemSQLFactory:
    return ItemSQLFactory(faker=faker, context=sql_context)


@pytest.fixture
def item_mongo_factory(faker: Faker, mongo_context: MongoDBContext) -> ItemMongoFactory:
    return ItemMongoFactory(faker=faker, context=mongo_context)


@pytest.fixture
def user_factory(faker: Faker, sql_context: SQLContext) -> UserSQLFactory:
    return UserSQLFactory(faker=faker, context=sql_context)


@pytest.fixture
def post_factory(faker: Faker, sql_context: SQLContext) -> PostSQLFactory:
    return PostSQLFactory(faker=faker, context=sql_context)
