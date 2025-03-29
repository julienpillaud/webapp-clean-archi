import logging
from collections.abc import Callable, Iterator
from contextlib import contextmanager
from functools import wraps
from typing import Concatenate, ParamSpec, Protocol, TypeVar

from app.domain.context import ContextProtocol
from app.domain.exceptions import DomainError
from app.domain.post.commands import (
    create_post_command,
    delete_post_command,
    get_post_command,
    get_posts_command,
    update_post_command,
)
from app.domain.user.commands import (
    create_user_command,
    delete_user_command,
    get_user_command,
    get_users_command,
    update_user_command,
)

logger = logging.getLogger(__name__)

P = ParamSpec("P")
R = TypeVar("R")


class UnitOfWorkProtocol(Protocol):
    @contextmanager
    def transaction(self) -> Iterator[None]: ...
    def commit(self) -> None: ...
    def rollback(self) -> None: ...


class TransactionalContextProtocol(UnitOfWorkProtocol, ContextProtocol): ...


class Domain:
    def _command_handler(
        self, func: Callable[Concatenate[TransactionalContextProtocol, P], R]
    ) -> Callable[P, R]:
        @wraps(func)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
            with self.context.transaction():
                try:
                    result = func(self.context, *args, **kwargs)
                except DomainError as error:
                    self.context.rollback()
                    logger.info(f"Domain error: {error} - Rolling back transaction")
                    raise error

                self.context.commit()
                return result

        return wrapper

    def __init__(self, context: TransactionalContextProtocol):
        self.context = context

        self.create_post = self._command_handler(create_post_command)
        self.delete_post = self._command_handler(delete_post_command)
        self.get_post = self._command_handler(get_post_command)
        self.get_posts = self._command_handler(get_posts_command)
        self.update_post = self._command_handler(update_post_command)

        self.create_user = self._command_handler(create_user_command)
        self.delete_user = self._command_handler(delete_user_command)
        self.get_user = self._command_handler(get_user_command)
        self.get_users = self._command_handler(get_users_command)
        self.update_user = self._command_handler(update_user_command)
