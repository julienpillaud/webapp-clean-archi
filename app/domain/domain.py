import logging
import time
from collections.abc import Callable, Iterator
from contextlib import contextmanager
from functools import wraps
from typing import Concatenate, Generic, ParamSpec, Protocol, TypeVar

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
    authenticate_user_command,
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


class CommandHandler(Generic[P, R]):
    def __init__(
        self, func: Callable[Concatenate[TransactionalContextProtocol, P], R]
    ) -> None:
        self.func = func

    def __get__(self, instance: "Domain", owner: type["Domain"]) -> Callable[P, R]:
        logger.debug(f"Command '{self.func.__name__}' bound")
        return instance.command_handler(self.func)


class Domain:
    get_posts = CommandHandler(get_posts_command)
    get_post = CommandHandler(get_post_command)
    create_post = CommandHandler(create_post_command)
    update_post = CommandHandler(update_post_command)
    delete_post = CommandHandler(delete_post_command)

    authenticate_user = CommandHandler(authenticate_user_command)
    get_users = CommandHandler(get_users_command)
    get_user = CommandHandler(get_user_command)
    create_user = CommandHandler(create_user_command)
    update_user = CommandHandler(update_user_command)
    delete_user = CommandHandler(delete_user_command)

    unexpected_error = CommandHandler(unexpected_error_command)
    unexpected_domain_error = CommandHandler(unexpected_domain_error_command)

    def __init__(self, context: TransactionalContextProtocol):
        logger.info("Instantiate Domain")
        self.context = context

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
