import uuid
from typing import Any

from app.domain.users.entities import User
from app.infrastructure.sql.models import OrmUser
from tests.fixtures.factories.sql import SqlBaseFactory


class UserSqlFactory(SqlBaseFactory[User, OrmUser]):
    def _build_entity(self, **kwargs: Any) -> User:
        return User(
            id=uuid.uuid4(),
            username=kwargs.get("username", self.faker.user_name()),
            email=kwargs.get("email", self.faker.unique.email()),
            posts=[],
        )

    def _to_database_entity(self, entity: User) -> OrmUser:
        return OrmUser(
            id=entity.id,
            username=entity.username,
            email=entity.email,
        )
