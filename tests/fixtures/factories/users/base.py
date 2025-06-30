from typing import Any

from faker import Faker

from app.core.security import get_password_hash
from app.domain.users.entities import User
from tests.fixtures.factories.base import BaseFactory


class UserBaseFactory(BaseFactory[User]):
    def __init__(self) -> None:
        self.faker = Faker()

    def _build_entity(self, **kwargs: Any) -> User:
        plain_password = kwargs.get("password", self.faker.password())
        hashed_password = get_password_hash(plain_password)

        return User(
            id=None,
            email=kwargs.get("email", self.faker.unique.email()),
            username=kwargs.get("username", self.faker.user_name()),
            hashed_password=kwargs.get("hashed_password", hashed_password),
            posts=[],
        )
