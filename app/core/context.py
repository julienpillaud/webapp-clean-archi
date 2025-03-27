from app.core.config import Settings
from app.domain.domain import TransactionalContextProtocol
from app.infrastructure.repository.user import UserSqlRepository
from app.infrastructure.sqlalchemy_uow import SqlAlchemyUnitOfWork


class Context(SqlAlchemyUnitOfWork, TransactionalContextProtocol):
    def __init__(self, settings: Settings):
        super().__init__(settings)

    @property
    def user_repository(self):
        return UserSqlRepository(session=self.session)
