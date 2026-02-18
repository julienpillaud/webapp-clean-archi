import pytest
from faker import Faker
from pymongo.database import Database
from sqlalchemy.orm import Session

from app.infrastructure.mongo.base import MongoDocument
from tests.factories.dummies import DummySQLFactory
from tests.factories.items import ItemMongoFactory, ItemSQLFactory
from tests.factories.posts import PostSQLFactory
from tests.factories.users import UserSQLFactory


@pytest.fixture
def faker() -> Faker:
    return Faker()


@pytest.fixture
def dummy_factory(faker: Faker, session: Session) -> DummySQLFactory:
    return DummySQLFactory(faker=faker, session=session)


@pytest.fixture
def item_sql_factory(faker: Faker, session: Session) -> ItemSQLFactory:
    return ItemSQLFactory(faker=faker, session=session)


@pytest.fixture
def item_mongo_factory(
    faker: Faker,
    mongo_database: Database[MongoDocument],
) -> ItemMongoFactory:
    return ItemMongoFactory(faker=faker, database=mongo_database)


@pytest.fixture
def user_factory(faker: Faker, session: Session) -> UserSQLFactory:
    return UserSQLFactory(faker=faker, session=session)


@pytest.fixture
def post_factory(faker: Faker, session: Session) -> PostSQLFactory:
    return PostSQLFactory(faker=faker, session=session)
