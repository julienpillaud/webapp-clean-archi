import uuid
from typing import Any

from app.domain.users.entities import User
from app.infrastructure.sql.users import UserSQLRepository
from tests.factories.base import BaseSQLFactory
from tests.factories.faker import faker


def generate_user(**kwargs: Any) -> User:  # noqa: ANN401
    return User(
        id=uuid.uuid7(),
        email=kwargs.get("email", "user@mail.fr"),
        username=kwargs.get("username", faker.random_string()),
        posts=[],
    )


class UserSQLFactory(BaseSQLFactory[User]):
    def build(self, **kwargs: Any) -> User:  # noqa: ANN401
        return generate_user(**kwargs)

    @property
    def _repository(self) -> UserSQLRepository:
        return UserSQLRepository(session=self.session)
