import time
from collections.abc import Callable
from types import TracebackType
from typing import Concatenate, Protocol

from app.core.logger import logger
from app.domain.context import ContextProtocol


class TransactionProtocol(Protocol):
    def start(self) -> None: ...

    def end(self, error: BaseException | None) -> None: ...


class Domain:
    def __init__(self, context: ContextProtocol) -> None:
        self._context = context

    def run[**P, R](
        self,
        func: Callable[Concatenate[ContextProtocol, P], R],
        /,
        *args: P.args,
        **kwargs: P.kwargs,
    ) -> R:
        name = getattr(func, "__name__", "unknown")
        start_time = time.perf_counter()
        try:
            return func(self._context, *args, **kwargs)
        finally:
            elapsed = (time.perf_counter() - start_time) * 1000
            logger.info(f"{name} [{elapsed:.1f} ms]")


class DomainContext:
    def __init__(
        self,
        transaction: TransactionProtocol,
        context_provider: Callable[[TransactionProtocol], ContextProtocol],
    ) -> None:
        self._transaction = transaction
        self._context_provider = context_provider

    def __enter__(self) -> Domain:
        logger.debug("Start Use case")
        self._start_time = time.perf_counter()
        self._transaction.start()
        self._context = self._context_provider(self._transaction)
        self._domain = Domain(context=self._context)
        return self._domain

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        self._transaction.end(error=exc_val)
        elapsed = (time.perf_counter() - self._start_time) * 1000
        logger.info(f"Use case [{elapsed:.1f} ms]")
