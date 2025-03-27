import logging
from collections.abc import Iterator

import pytest
from sqlalchemy import Engine, create_engine
from sqlalchemy.orm import Session

from app.core.config import Settings
from app.infrastructure.repository.models import OrmBase

logger = logging.getLogger(__name__)


@pytest.fixture(scope="session")
def engine(settings: Settings) -> Engine:
    logger.info(f"Create engine {settings.SQLALCHEMY_DATABASE_URI}")
    return create_engine(str(settings.SQLALCHEMY_DATABASE_URI))


@pytest.fixture(scope="session")
def setup_db(engine: Engine) -> None:
    logger.info("Drop all tables")
    OrmBase.metadata.drop_all(engine)
    logger.info("Create all tables")
    OrmBase.metadata.create_all(engine)


@pytest.fixture
def session(setup_db: None, engine: Engine) -> Iterator[Session]:
    with Session(engine, expire_on_commit=False) as session:
        logger.debug("Creating session")
        yield session

        session.rollback()
        logger.debug("Deleting database tables")
        for table in reversed(OrmBase.metadata.sorted_tables):
            session.execute(table.delete())
        session.commit()
