import uuid
from typing import Any

from faker import Faker

from app.core.security import get_password_hash
from app.domain.users.entities import User
from app.infrastructure.sql.models import OrmUser
from app.infrastructure.sql.users import UserSqlRepository
from tests.factories.base import BaseSqlFactory


def generate_user(faker: Faker, **kwargs: Any) -> User:
    return User(
        id=uuid.uuid7(),
        email=kwargs["email"] if "email" in kwargs else faker.email(),
        username=kwargs["username"] if "username" in kwargs else faker.name(),
        hashed_password=kwargs["hashed_password"]
        if "hashed_password" in kwargs
        else get_password_hash("password"),
        posts=[],
    )


class UserFactory(BaseSqlFactory[User, OrmUser]):
    repository_class = UserSqlRepository

    def build(self, **kwargs: Any) -> User:
        if "password" in kwargs:
            kwargs["hashed_password"] = get_password_hash(kwargs["password"])
        return generate_user(faker=self.faker, **kwargs)
