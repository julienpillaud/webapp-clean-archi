from typing import Any, Generic, TypeVar

import pytest
from faker import Faker
from sqlalchemy.orm import Session

from app.infrastructure.repository.models import OrmPost, OrmTag, OrmUser

T = TypeVar("T")


class BaseFactory(Generic[T]):
    def __init__(self, session: Session):
        self.session = session
        self.faker = Faker()

    def create_one(self, **kwargs: Any) -> T:
        instance = self._make(**kwargs)
        self._create([instance])
        return instance

    def create_many(self, count: int, /, **kwargs: Any) -> list[T]:
        instances = [self._make(**kwargs) for _ in range(count)]
        self._create(instances)
        return instances

    def _create(self, instances: list[T]) -> None:
        self.session.add_all(instances)
        self.session.commit()

    def _make(self, **kwargs: Any) -> T:
        raise NotImplementedError


class UserFactory(BaseFactory[OrmUser]):
    def __init__(self, session: Session):
        super().__init__(session)

    def _make(self, **kwargs: Any) -> OrmUser:
        return OrmUser(
            username=kwargs.get("username", self.faker.user_name()),
            email=kwargs.get("email", self.faker.unique.email()),
        )


class PostFactory(BaseFactory[OrmPost]):
    def __init__(self, session: Session, user_factory: UserFactory):
        super().__init__(session)
        self.user_factory = user_factory

    def _make(self, **kwargs: Any) -> OrmPost:
        if not (author_id := kwargs.get("author_id")):
            author_id = self.user_factory.create_one().id

        if not (tags := kwargs.get("tags")):
            num_tags = self.faker.random_int(min=1, max=3)
            tags = [
                OrmTag(name=f"{self.faker.unique.lexify(text='?????')}{i}")
                for i in range(num_tags)
            ]

        return OrmPost(
            title=kwargs.get("title", self.faker.sentence()),
            content=kwargs.get("content", self.faker.text()),
            author_id=author_id,
            tags=tags,
        )


@pytest.fixture
def faker() -> Faker:
    return Faker()


@pytest.fixture
def user_factory(session: Session) -> UserFactory:
    return UserFactory(session=session)


@pytest.fixture
def post_factory(session: Session, user_factory: UserFactory) -> PostFactory:
    return PostFactory(session=session, user_factory=user_factory)
