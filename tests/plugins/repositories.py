import pytest
from sqlalchemy.orm import Session

from app.infrastructure.sql.posts import PostSQLRepository


@pytest.fixture
def post_repository(session: Session) -> PostSQLRepository:
    return PostSQLRepository(session=session)
