import pytest
from pymongo.database import Database
from sqlalchemy.orm import Session

from app.core.config import DatabaseType, Settings
from app.infrastructure.mongo.base import MongoDocument
from tests.fixtures.factories.posts.base import PostBaseFactory
from tests.fixtures.factories.posts.mongo import PostMongoFactory
from tests.fixtures.factories.posts.sql import PostSqlFactory
from tests.fixtures.factories.users.base import UserBaseFactory
from tests.fixtures.factories.users.mongo import UserMongoFactory
from tests.fixtures.factories.users.sql import UserSqlFactory


@pytest.fixture
def user_sql_factory(session: Session) -> UserSqlFactory:
    return UserSqlFactory(session=session)


@pytest.fixture
def user_mongo_factory(mongo_db: Database[MongoDocument]) -> UserMongoFactory:
    return UserMongoFactory(collection=mongo_db["users"])


@pytest.fixture
def user_factory(
    settings: Settings,
    user_sql_factory: UserSqlFactory,
    user_mongo_factory: UserMongoFactory,
) -> UserBaseFactory:
    match settings.database_type:
        case DatabaseType.SQL:
            return user_sql_factory
        case DatabaseType.MONGO:
            return user_mongo_factory


@pytest.fixture
def post_sql_factory(
    session: Session, user_sql_factory: UserSqlFactory
) -> PostSqlFactory:
    return PostSqlFactory(session=session, user_factory=user_sql_factory)


@pytest.fixture
def post_mongo_factory(
    mongo_db: Database[MongoDocument],
    user_mongo_factory: UserMongoFactory,
) -> PostMongoFactory:
    return PostMongoFactory(
        collection=mongo_db["posts"],
        user_factory=user_mongo_factory,
    )


@pytest.fixture
def post_factory(
    settings: Settings,
    post_sql_factory: PostSqlFactory,
    post_mongo_factory: PostMongoFactory,
) -> PostBaseFactory:
    match settings.database_type:
        case DatabaseType.SQL:
            return post_sql_factory
        case DatabaseType.MONGO:
            return post_mongo_factory


# @pytest.fixture
# def generic_entity_mongo_factory(
#     mongo_db: Database[MongoDocument],
# ) -> GenericEntityMongoFactory:
#     return GenericEntityMongoFactory(collection=mongo_db["generics"])
