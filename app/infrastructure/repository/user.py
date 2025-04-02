from sqlalchemy import select

from app.domain.users.entities import User
from app.domain.users.repository import UserRepositoryProtocol
from app.infrastructure.repository.base import BaseSqlRepository
from app.infrastructure.repository.models import OrmUser


class UserSqlRepository(
    BaseSqlRepository[User, OrmUser],
    UserRepositoryProtocol,
):
    domain_model = User
    orm_model = OrmUser

    def get_by_email(self, email: str) -> User | None:
        stmt = select(OrmUser).where(OrmUser.email == email)
        orm_entity = self.session.execute(stmt).scalar_one_or_none()
        return self.orm_to_domain_entity(orm_entity=orm_entity) if orm_entity else None
