from typing import Any

from app.core.security import get_password_hash
from app.domain.users.entities import User
from factories.base import BaseFactory
from factories.factories import UserFactory


class UserBaseFactory(BaseFactory[User]):
    def _build_entity(self, **kwargs: Any) -> User:
        if "password" in kwargs:
            kwargs["hashed_password"] = get_password_hash(kwargs["password"])
        return UserFactory.build(**kwargs)
