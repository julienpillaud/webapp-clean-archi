import pytest
from faker import Faker
from sqlalchemy.orm import Session

from tests.factories.posts import PostFactory
from tests.factories.users import UserFactory


@pytest.fixture
def faker() -> Faker:
    return Faker()


@pytest.fixture
def user_factory(faker: Faker, session: Session) -> UserFactory:
    return UserFactory(faker=faker, session=session)


@pytest.fixture
def post_factory(faker: Faker, session: Session) -> PostFactory:
    return PostFactory(faker=faker, session=session)
