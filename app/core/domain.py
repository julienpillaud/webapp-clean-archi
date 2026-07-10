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
        self.command_name = ""

    def run[**P, R](
        self,
        command: Callable[Concatenate[ContextProtocol, P], R],
        /,
        *args: P.args,
        **kwargs: P.kwargs,
    ) -> R:
        self.command_name = getattr(command, "__name__", "unknown")
        return command(self.context, *args, **kwargs)

    def __enter__(self) -> Domain:
        self._start = time.perf_counter()
        self._session = self.resource.start_transaction()
        self.context = self.context_factory(self._session)
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        self.resource.end_transaction(self._session, exc_val)
        elapsed = (time.perf_counter() - self._start) * 1000
        logger.info(f"'{self.command_name}' executed in {elapsed:.1f} ms")
