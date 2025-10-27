from typing import Any, ClassVar

from cleanstack.factories.sql import SqlBaseFactory
from polyfactory.factories.pydantic_factory import ModelFactory
from sqlalchemy.orm import Session

from app.core.security import get_password_hash
from app.domain.posts.entities import Post
from app.domain.users.entities import User
from app.infrastructure.sql.models import OrmUser


class UserEntityFactory(ModelFactory[User]):
    __check_model__ = True
    posts: ClassVar[list[Post]] = []


class UserFactory(SqlBaseFactory[User, OrmUser]):
    orm_model = OrmUser

    def __init__(self, session: Session) -> None:
        super().__init__(session=session)

    def _build_entity(self, **kwargs: Any) -> User:
        if "password" in kwargs:
            kwargs["hashed_password"] = get_password_hash(kwargs["password"])
        return UserEntityFactory.build(**kwargs)
