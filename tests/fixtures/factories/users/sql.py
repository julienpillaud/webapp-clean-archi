from sqlalchemy.orm import Session

from app.domain.users.entities import User
from app.infrastructure.sql.models import OrmUser
from tests.fixtures.factories.sql import SqlBaseFactory
from tests.fixtures.factories.users.base import UserBaseFactory


class UserSqlFactory(SqlBaseFactory[User, OrmUser], UserBaseFactory):
    def __init__(self, session: Session) -> None:
        SqlBaseFactory.__init__(self, session=session)
        UserBaseFactory.__init__(self)

    def _to_database_entity(self, entity: User) -> OrmUser:
        return OrmUser(
            id=entity.id,
            username=entity.username,
            email=entity.email,
        )
