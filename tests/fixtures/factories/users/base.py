from typing import Any

from faker import Faker

from app.domain.users.entities import User
from tests.fixtures.factories.base import BaseFactory


class UserBaseFactory(BaseFactory[User]):
    def __init__(self) -> None:
        self.faker = Faker()

    def _build_entity(self, **kwargs: Any) -> User:
        return User(
            id=None,
            username=kwargs.get("username", self.faker.user_name()),
            email=kwargs.get("email", self.faker.unique.email()),
            posts=[],
        )
