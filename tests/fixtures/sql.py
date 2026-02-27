from collections.abc import Iterator

import pytest
from sqlalchemy import Engine
from sqlalchemy.orm import Session, sessionmaker

from app.core.config import Settings
from app.infrastructure.sql.entities import OrmEntity
from app.infrastructure.sql.uow import SQLContext


def clean(engine: Engine) -> None:
    with Session(engine) as session:
        for table in reversed(OrmEntity.metadata.sorted_tables):
            session.execute(table.delete())
        session.commit()


@pytest.fixture(scope="session")
def sql_context_init(settings: Settings) -> SQLContext:
    context = SQLContext.from_settings(dsn=str(settings.postgres_dsn))
    engine = context.engine

    OrmEntity.metadata.drop_all(engine)
    OrmEntity.metadata.create_all(engine)

    return context


@pytest.fixture
def sql_context(sql_context_init: SQLContext) -> Iterator[SQLContext]:
    yield sql_context_init
    clean(sql_context_init.engine)


@pytest.fixture
def session_factory(sql_context_init: SQLContext) -> Iterator[sessionmaker[Session]]:
    yield sql_context_init.session_factory
    clean(sql_context_init.engine)


@pytest.fixture
def session(sql_context_init: SQLContext) -> Iterator[Session]:
    engine = sql_context_init.engine
    with Session(engine) as session:
        yield session
    clean(engine)
