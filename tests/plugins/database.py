from collections.abc import Iterator

import pytest
from cleanstack.sql.entities import OrmEntity
from sqlalchemy.orm import Session

from app.core.config import Settings
from app.infrastructure.sql.resource import SQLResource


@pytest.fixture(scope="session")
def init_resource(settings: Settings) -> Iterator[SQLResource]:
    resource = SQLResource.from_settings(settings)
    OrmEntity.metadata.drop_all(resource.engine)
    OrmEntity.metadata.create_all(resource.engine)

    yield resource

    resource.release()


@pytest.fixture
def db_resource(init_resource: SQLResource) -> Iterator[SQLResource]:
    yield init_resource

    init_resource.reset()


@pytest.fixture
def session(db_resource: SQLResource) -> Iterator[Session]:
    with db_resource.session_factory() as session:
        yield session
