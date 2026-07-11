import logging
import time
from collections.abc import Callable
from types import TracebackType
from typing import Concatenate

from app.core.context import ContextFactory
from app.domain.context import ContextProtocol
from app.infrastructure.sql.utils import SQLResource

logger = logging.getLogger("app")


class Domain:
    def __init__(
        self,
        resource: SQLResource,
        context_factory: ContextFactory,
    ) -> None:
        self.resource = resource
        self.context_factory = context_factory
        self._context: ContextProtocol | None = None
        self._func_name = "unknown"
        self._is_mutation = False

    @property
    def context(self) -> ContextProtocol:
        if self._context is None:
            raise RuntimeError("Domain must be used as a context manager")

        return self._context

    def query[**P, R](
        self,
        func: Callable[Concatenate[ContextProtocol, P], R],
        /,
        *args: P.args,
        **kwargs: P.kwargs,
    ) -> R:
        self._func_name = getattr(func, "__name__", "unknown")
        self._is_mutation = False
        return func(self.context, *args, **kwargs)

    def command[**P, R](
        self,
        func: Callable[Concatenate[ContextProtocol, P], R],
        /,
        *args: P.args,
        **kwargs: P.kwargs,
    ) -> R:
        self._func_name = getattr(func, "__name__", "unknown")
        self._is_mutation = True
        return func(self.context, *args, **kwargs)

    def __enter__(self) -> Domain:
        self._start = time.perf_counter()
        self._session = self.resource.start_transaction()
        self._context = self.context_factory(self._session)
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        self.resource.end_transaction(
            session=self._session,
            exc_val=exc_val,
            is_mutation=self._is_mutation,
        )
        elapsed = (time.perf_counter() - self._start) * 1000
        logger.info(f"'{self._func_name}' executed in {elapsed:.1f} ms")
