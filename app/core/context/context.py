from app.core.context.sql import SqlContext
from app.domain.dummies.repository import DummyRepositoryProtocol
from app.domain.posts.repository import PostRepositoryProtocol
from app.domain.users.repository import UserRepositoryProtocol
from app.infrastructure.sql.dummies import DummySqlRepository
from app.infrastructure.sql.posts import PostSqlRepository
from app.infrastructure.sql.users import UserSqlRepository


class Context(SqlContext):
    @property
    def dummy_repository(self) -> DummyRepositoryProtocol:
        return DummySqlRepository(session=self.session)

    @property
    def post_repository(self) -> PostRepositoryProtocol:
        return PostSqlRepository(session=self.session)

    @property
    def user_repository(self) -> UserRepositoryProtocol:
        return UserSqlRepository(session=self.session)
