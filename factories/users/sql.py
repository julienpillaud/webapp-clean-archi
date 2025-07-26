from sqlalchemy.orm import Session

from app.domain.users.entities import User
from app.infrastructure.sql.models import OrmUser
from factories.sql import SqlBaseFactory
from factories.users.base import UserBaseFactory


class UserSqlFactory(SqlBaseFactory[User, OrmUser], UserBaseFactory):
    def __init__(self, session: Session) -> None:
        SqlBaseFactory.__init__(self, session=session)

    def _to_database_entity(self, entity: User) -> OrmUser:
        return OrmUser(
            id=entity.id,
            email=entity.email,
            username=entity.username,
            hashed_password=entity.hashed_password,
        )
