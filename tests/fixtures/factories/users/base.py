import uuid
from typing import Any

from app.core.security import get_password_hash
from app.domain.users.entities import User
from tests.fixtures.factories.base import BaseFactory, faker


class UserBaseFactory(BaseFactory[User]):
    def _build_entity(self, hash_password: bool = False, **kwargs: Any) -> User:
        plain_password = kwargs.get("password", faker.password())
        hashed_password = (
            get_password_hash(plain_password) if hash_password else "fake-hash"
        )

        return User(
            id=uuid.uuid4(),
            email=kwargs.get("email", faker.unique.email()),
            username=kwargs.get("username", faker.user_name()),
            hashed_password=kwargs.get("hashed_password", hashed_password),
            posts=[],
        )
