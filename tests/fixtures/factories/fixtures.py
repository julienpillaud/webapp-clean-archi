import pytest
from faker import Faker
from pymongo.database import Database
from sqlalchemy.orm import Session

from app.infrastructure.mongo.base import MongoDocument
from tests.fixtures.factories.generics import GenericEntityMongoFactory
from tests.fixtures.factories.posts import PostSqlFactory
from tests.fixtures.factories.users import UserSqlFactory


@pytest.fixture
def faker() -> Faker:
    return Faker()


@pytest.fixture
def user_sql_factory(session: Session) -> UserSqlFactory:
    return UserSqlFactory(session=session)


@pytest.fixture
def post_sql_factory(
    session: Session, user_sql_factory: UserSqlFactory
) -> PostSqlFactory:
    return PostSqlFactory(session=session, user_factory=user_sql_factory)


@pytest.fixture
def generic_entity_mongo_factory(
    mongo_db: Database[MongoDocument],
) -> GenericEntityMongoFactory:
    return GenericEntityMongoFactory(collection=mongo_db["generics"])
