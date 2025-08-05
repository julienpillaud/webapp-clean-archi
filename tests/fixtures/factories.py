import pytest
from sqlalchemy.orm import Session

from factories.posts import PostFactory
from factories.users import UserFactory


@pytest.fixture
def user_factory(session: Session) -> UserFactory:
    return UserFactory(session=session)


@pytest.fixture
def post_factory(session: Session) -> PostFactory:
    return PostFactory(session=session)
