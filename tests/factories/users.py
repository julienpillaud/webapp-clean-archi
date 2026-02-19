import uuid
from typing import Any

from faker import Faker

from app.domain.users.entities import User
from app.domain.users.repository import UserRepositoryProtocol
from app.infrastructure.sql.repositories.users import UserSQLRepository
from tests.factories.base import BaseSQLFactory


def generate_user(faker: Faker, **kwargs: Any) -> User:
    return User(
        id=uuid.uuid7(),
        provider_id=kwargs["provider_id"]
        if "provider_id" in kwargs
        else str(uuid.uuid7()),
        email=kwargs["email"] if "email" in kwargs else faker.email(),
        username=kwargs["username"] if "username" in kwargs else faker.name(),
        posts=[],
    )


class UserSQLFactory(BaseSQLFactory[User]):
    def build(self, **kwargs: Any) -> User:
        return generate_user(faker=self.faker, **kwargs)

    @property
    def repository(self) -> UserRepositoryProtocol:
        return UserSQLRepository(session=self.session)
