import logging
import time
from collections.abc import Callable, Iterator
from contextlib import contextmanager
from functools import wraps
from typing import Concatenate, ParamSpec, Protocol, TypeVar

from app.domain.context import ContextProtocol
from app.domain.dev.commands import (
    unexpected_domain_error_command,
    unexpected_error_command,
)
from app.domain.posts.commands import (
    create_post_command,
    delete_post_command,
    get_post_command,
    get_posts_command,
    update_post_command,
)
from app.domain.users.commands import (
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
    def command_handler(
        self, func: Callable[Concatenate[TransactionalContextProtocol, P], R]
    ) -> Callable[P, R]:
        @wraps(func)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
            start_time = time.perf_counter()
            with self.context.transaction():
                try:
                    result = func(self.context, *args, **kwargs)
                # Catch all exceptions to ensure rollback
                except Exception as error:
                    self.context.rollback()
                    logger.debug(
                        f"Command '{func.__name__}' failed with "
                        f"{error.__class__.__name__}: {error}"
                    )
                    raise

                self.context.commit()
                duration = time.perf_counter() - start_time
                logger.debug(
                    f"Command '{func.__name__}' succeeded in {duration * 1000:.1f} ms",
                )
                return result

        return wrapper

    def __init__(self, context: TransactionalContextProtocol):
        self.context = context

        self.create_post = self.command_handler(create_post_command)
        self.delete_post = self.command_handler(delete_post_command)
        self.get_post = self.command_handler(get_post_command)
        self.get_posts = self.command_handler(get_posts_command)
        self.update_post = self.command_handler(update_post_command)

        self.create_user = self.command_handler(create_user_command)
        self.delete_user = self.command_handler(delete_user_command)
        self.get_user = self.command_handler(get_user_command)
        self.get_users = self.command_handler(get_users_command)
        self.update_user = self.command_handler(update_user_command)

        self.unexpected_error = self.command_handler(unexpected_error_command)
        self.unexpected_domain_error = self.command_handler(
            unexpected_domain_error_command
        )
