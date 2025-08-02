from app.core.context.sql import SqlContext
from app.domain.interfaces.task_queue import TaskQueueProtocol
from app.domain.posts.repository import PostRepositoryProtocol
from app.domain.users.repository import UserRepositoryProtocol
from app.infrastructure.celery_task_queue.celery_task_queue import CeleryTaskQueue
from app.infrastructure.sql.posts import PostSqlRepository
from app.infrastructure.sql.users import UserSqlRepository


class Context(SqlContext):
    @property
    def post_repository(self) -> PostRepositoryProtocol:
        return PostSqlRepository(session=self.session)

    @property
    def user_repository(self) -> UserRepositoryProtocol:
        return UserSqlRepository(session=self.session)

    @property
    def task_queue(self) -> TaskQueueProtocol:
        return CeleryTaskQueue(settings=self.settings)
