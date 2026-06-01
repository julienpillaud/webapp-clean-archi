import uuid
from typing import Any

from cleanstack.factories.sql import BaseSQLFactory

from app.domain.users.entities import User
from app.infrastructure.sql.users import UserSQLRepository
from tests.factories.faker import faker


def generate_user(**kwargs: Any) -> User:
    return User(
        id=uuid.uuid7(),
        provider_id=kwargs.get("provider_id", str(uuid.uuid7())),
        email=kwargs.get("email", "user@mail.fr"),
        username=kwargs.get("username", faker.random_string()),
        posts=[],
    )


class UserSQLFactory(BaseSQLFactory[User]):
    def build(self, **kwargs: Any) -> User:
        return generate_user(**kwargs)

    @property
    def _repository(self) -> UserSQLRepository:
        return UserSQLRepository(session=self.session)
