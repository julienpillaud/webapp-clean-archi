from typing import cast

import pytest
from pymongo.database import Database
from sqlalchemy.orm import Session

from app.core.config import DatabaseType, Settings
from app.infrastructure.mongo.base import MongoDocument
from factories.posts.base import PostBaseFactory
from factories.posts.mongo import PostMongoFactory
from factories.posts.sql import PostSqlFactory
from factories.users.base import UserBaseFactory
from factories.users.mongo import UserMongoFactory
from factories.users.sql import UserSqlFactory


@pytest.fixture
def user_sql_factory(session: Session) -> UserSqlFactory:
    return UserSqlFactory(session=session)


@pytest.fixture
def user_mongo_factory(mongo_db: Database[MongoDocument]) -> UserMongoFactory:
    return UserMongoFactory(collection=mongo_db["users"])


@pytest.fixture
def user_factory(
    request: pytest.FixtureRequest,
    settings: Settings,
) -> UserBaseFactory:
    match settings.database_type:
        case DatabaseType.SQL:
            user_sql_factory = request.getfixturevalue("user_sql_factory")
            return cast(UserBaseFactory, user_sql_factory)
        case DatabaseType.MONGO:
            user_mongo_factory = request.getfixturevalue("user_mongo_factory")
            return cast(UserBaseFactory, user_mongo_factory)


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
    request: pytest.FixtureRequest,
    settings: Settings,
) -> PostBaseFactory:
    match settings.database_type:
        case DatabaseType.SQL:
            post_sql_factory = request.getfixturevalue("post_sql_factory")
            return cast(PostBaseFactory, post_sql_factory)
        case DatabaseType.MONGO:
            post_mongo_factory = request.getfixturevalue("post_mongo_factory")
            return cast(PostBaseFactory, post_mongo_factory)
