import time
from collections.abc import Callable
from types import TracebackType
from typing import Concatenate, Protocol

from app.core.logger import logger
from app.domain.context import ContextProtocol


class ResourceProtocol(Protocol):
    def start_transaction(self, transactional: bool) -> None: ...

    def end_transaction(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        transactional: bool,
    ) -> None: ...


class Domain:
    def __init__(self, context: ContextProtocol) -> None:
        self.context = context

    def run[**P, R](
        self,
        func: Callable[Concatenate[ContextProtocol, P], R],
        /,
        *args: P.args,
        **kwargs: P.kwargs,
    ) -> R:
        name = getattr(func, "__name__", "unknown")
        start = time.perf_counter()
        try:
            return func(self.context, *args, **kwargs)
        finally:
            elapsed = (time.perf_counter() - start) * 1000
            logger.info(f"{name} [{elapsed:.1f} ms]")

    def __repr__(self) -> str:
        return f"{self.__class__.__name__} ({id(self)})"


class DomainManager:
    def __init__(
        self,
        resource: ResourceProtocol,
        context_provider: Callable[[ResourceProtocol], ContextProtocol],
        transactional: bool = False,
    ) -> None:
        self._resource = resource
        self._context_provider = context_provider
        self._transactional = transactional

    def __enter__(self) -> Domain:
        self._resource.start_transaction(transactional=self._transactional)
        self._context = self._context_provider(self._resource)
        self._domain = Domain(context=self._context)
        logger.debug(f"{self._domain} (Enter)")
        return self._domain

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        self._resource.end_transaction(
            exc_type=exc_type,
            exc_val=exc_val,
            transactional=self._transactional,
        )
        logger.debug(f"{self._domain} (Exit)")
