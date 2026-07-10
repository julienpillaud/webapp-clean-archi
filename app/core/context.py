from collections.abc import Callable
from functools import cached_property

from sqlalchemy.orm import Session

from app.core.config import Settings
from app.domain.context import ContextProtocol
from app.domain.posts.repository import PostRepositoryProtocol
from app.domain.users.repository import UserRepositoryProtocol
from app.infrastructure.sql.posts import PostSQLRepository
from app.infrastructure.sql.users import UserSQLRepository

type ContextFactory = Callable[[Session], ContextProtocol]


class Context(ContextProtocol):
    def __init__(self, settings: Settings, session: Session) -> None:
        self.settings = settings
        self.session = session

    @cached_property
    def post_repository(self) -> PostRepositoryProtocol:
        return PostSQLRepository(session=self.session)

    @cached_property
    def user_repository(self) -> UserRepositoryProtocol:
        return UserSQLRepository(session=self.session)
