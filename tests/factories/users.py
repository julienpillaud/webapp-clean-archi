import uuid
from typing import Any

from cleanstack.factories.sql import BaseSQLFactory

from app.domain.users.entities import User
from app.infrastructure.sql.users import UserSQLRepository


def generate_user(**kwargs: Any) -> User:
    return User(
        id=uuid.uuid7(),
        provider_id=kwargs.get("provider_id", str(uuid.uuid7())),
        email=kwargs.get("email", "user@mail.fr"),
        username=kwargs.get("username", "UserName"),
        posts=[],
    )


class UserSQLFactory(BaseSQLFactory[User]):
    def build(self, **kwargs: Any) -> User:
        return generate_user(**kwargs)

    @property
    def _repository(self) -> UserSQLRepository:
        return UserSQLRepository(session=self.uow.session)
