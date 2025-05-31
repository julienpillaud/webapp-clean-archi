import logging
from collections.abc import Callable

from app.core.config import DatabaseType, Settings
from app.domain.domain import TransactionalContextProtocol

logger = logging.getLogger(__name__)

context_registry: dict[DatabaseType, type[TransactionalContextProtocol]] = {}


class ContextContainer:
    _context_cls: type[TransactionalContextProtocol] | None = None

    @classmethod
    def set(cls, context_cls: type[TransactionalContextProtocol], /) -> None:
        cls._context_cls = context_cls

    @classmethod
    def get(cls) -> type[TransactionalContextProtocol]:
        if cls._context_cls is None:
            raise RuntimeError("Context not initialized")
        return cls._context_cls


def register_context(
    database_type: DatabaseType, /
) -> Callable[[type[TransactionalContextProtocol]], type[TransactionalContextProtocol]]:
    def decorator(
        cls: type[TransactionalContextProtocol],
    ) -> type[TransactionalContextProtocol]:
        context_registry[database_type] = cls
        return cls

    return decorator


def initialize_context(settings: Settings) -> None:
    if settings.database_type not in context_registry:
        raise RuntimeError("Invalid database type")

    context_cls = context_registry[settings.database_type]
    context_cls.initialize(settings=settings)
    ContextContainer.set(context_cls)
    logger.info(f"'{context_cls.__name__}' initialized")


def get_context() -> TransactionalContextProtocol:
    context_cls = ContextContainer.get()
    return context_cls()
