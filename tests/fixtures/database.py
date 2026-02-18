import logging
from collections.abc import Iterator

import pytest
from pymongo import MongoClient
from pymongo.database import Database
from sqlalchemy import Engine, create_engine
from sqlalchemy.orm import Session

from app.core.config import Settings
from app.infrastructure.mongo.base import MongoDocument
from app.infrastructure.sql.entities import OrmEntity

logger = logging.getLogger(__name__)


@pytest.fixture(scope="session")
def engine(settings: Settings) -> Engine:
    return create_engine(str(settings.postgres_dsn))


@pytest.fixture(scope="session")
def setup_db(engine: Engine) -> None:
    OrmEntity.metadata.drop_all(engine)
    OrmEntity.metadata.create_all(engine)


@pytest.fixture
def session(setup_db: None, engine: Engine) -> Iterator[Session]:
    with Session(engine) as session:
        yield session

    with Session(engine) as session:
        for table in reversed(OrmEntity.metadata.sorted_tables):
            session.execute(table.delete())
        session.commit()


@pytest.fixture(scope="session")
def mongo_client(settings: Settings) -> MongoClient[MongoDocument]:
    return MongoClient(
        settings.mongo_uri,
        uuidRepresentation="standard",
    )


@pytest.fixture(scope="session")
def mongo_database(
    settings: Settings,
    mongo_client: MongoClient[MongoDocument],
) -> Iterator[Database[MongoDocument]]:
    database = mongo_client[settings.mongo_database]
    yield database
    for collection in database.list_collection_names():
        database[collection].delete_many({})
