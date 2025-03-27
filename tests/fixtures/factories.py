from typing import Any, Generic, TypeVar

import pytest
from faker import Faker
from sqlalchemy.orm import Session

from app.infrastructure.repository.models import OrmUser

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


@pytest.fixture
def faker() -> Faker:
    return Faker()


@pytest.fixture
def user_factory(session: Session) -> UserFactory:
    return UserFactory(session=session)
