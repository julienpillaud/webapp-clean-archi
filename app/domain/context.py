from typing import Protocol

from cleanstack.domain import UnitOfWorkProtocol

from app.domain.interfaces.task_queue import TaskQueueProtocol
from app.domain.posts.repository import PostRepositoryProtocol
from app.domain.users.repository import UserRepositoryProtocol


class ContextProtocol(UnitOfWorkProtocol, Protocol):
    @property
    def post_repository(self) -> PostRepositoryProtocol: ...
    @property
    def user_repository(self) -> UserRepositoryProtocol: ...
    @property
    def task_queue(self) -> TaskQueueProtocol: ...
