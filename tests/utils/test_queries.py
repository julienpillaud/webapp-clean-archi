import pytest
from sqlalchemy import select
from sqlalchemy.orm import Session, joinedload, selectinload

from app.infrastructure.repository.models import OrmUser
from app.utils.sqlalchemy_instrument import SQLAlchemyInstrument
from tests.fixtures.factories import PostFactory, UserFactory

number_of_users = 10
numbers_of_test_users = 10
number_of_posts = 2


@pytest.fixture
def users(user_factory: UserFactory, post_factory: PostFactory) -> None:
    users = user_factory.create_many(number_of_users)
    test_users = user_factory.create_many(numbers_of_test_users, username="test")
    for user in users + test_users:
        post_factory.create_many(number_of_posts, author_id=user.id)


def test_select(session: Session, users: None) -> None:
    with SQLAlchemyInstrument.record() as instrument:
        stmt = select(OrmUser).where(OrmUser.username == "test")
        users_db = session.scalars(stmt).all()
        assert len(users_db) == numbers_of_test_users

        for user in users_db:
            assert len(user.posts) == number_of_posts

    # 1 query to fetch users and 1 query to fetch posts for each user
    assert instrument.queries_count == 1 + numbers_of_test_users


def test_selectinload(session: Session, users: None) -> None:
    with SQLAlchemyInstrument.record() as instrument:
        stmt = (
            select(OrmUser)
            .options(selectinload(OrmUser.posts))
            .where(OrmUser.username == "test")
        )
        users_db = session.scalars(stmt).all()
        assert len(users_db) == numbers_of_test_users

        for user in users_db:
            assert len(user.posts) == number_of_posts

    # 1 query to fetch users and 1 query to fetch posts
    assert instrument.queries_count == 2  # noqa


def test_joinedload(session: Session, users: None) -> None:
    with SQLAlchemyInstrument.record() as instrument:
        stmt = (
            select(OrmUser)
            .options(joinedload(OrmUser.posts))
            .where(OrmUser.username == "test")
        )
        # The unique() method must be invoked on this Result,
        # as it contains results that include joined eager loads against collections
        users_db = session.scalars(stmt).unique().all()
        assert len(users_db) == numbers_of_test_users

        for user in users_db:
            assert len(user.posts) == number_of_posts

    assert instrument.queries_count == 1
