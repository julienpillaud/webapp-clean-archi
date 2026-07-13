import logging
import time
from collections.abc import Callable
from dataclasses import dataclass
from types import TracebackType
from typing import Concatenate, Protocol, Self

from sqlalchemy.orm import Session

from app.domain.context import ContextProtocol

logger = logging.getLogger("app")


class ResourceProtocol[T](Protocol):
    def start_transaction(self) -> T: ...

    def end_transaction(
        self,
        session: T,
        exc_val: BaseException | None,
        is_mutation: bool,
    ) -> None: ...


@dataclass(frozen=True)
class DomainState[T]:
    session: T
    context: ContextProtocol


class BaseDomain[T]:
    def __init__(
        self,
        resource: ResourceProtocol[T],
        context_factory: Callable[[T], ContextProtocol],
    ) -> None:
        self.resource = resource
        self._context_factory = context_factory
        self._state: DomainState[T] | None = None
        self._use_case_timings: list[tuple[str, float]] = []
        self._is_mutation = False
        self._started = False

    @property
    def context(self) -> ContextProtocol:
        if not self._started:
            raise RuntimeError("Domain must be used as a context manager")

        if not self._state:
            _session = self.resource.start_transaction()
            _context = self._context_factory(_session)
            self._state = DomainState(session=_session, context=_context)

        return self._state.context

    def query[**P, R](
        self,
        func: Callable[Concatenate[ContextProtocol, P], R],
        /,
        *args: P.args,
        **kwargs: P.kwargs,
    ) -> R:
        return self._run(func, False, *args, **kwargs)

    def command[**P, R](
        self,
        func: Callable[Concatenate[ContextProtocol, P], R],
        /,
        *args: P.args,
        **kwargs: P.kwargs,
    ) -> R:
        return self._run(func, True, *args, **kwargs)

    def _run[**P, R](
        self,
        func: Callable[Concatenate[ContextProtocol, P], R],
        /,
        is_mutation: bool,
        *args: P.args,
        **kwargs: P.kwargs,
    ) -> R:
        name = getattr(func, "__name__", "unknown")
        if is_mutation:
            self._is_mutation = True  # once is True, never come back to False

        context = self.context
        start = time.perf_counter()
        try:
            return func(context, *args, **kwargs)
        finally:
            elapsed = (time.perf_counter() - start) * 1000
            self._use_case_timings.append((name, elapsed))

    def __enter__(self) -> Self:
        self._start = time.perf_counter()
        self._started = True
        logger.info("Enter Domain")
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        self._started = False

        if self._state:
            self.resource.end_transaction(
                session=self._state.session,
                exc_val=exc_val,
                is_mutation=self._is_mutation,
            )

        total_elapsed = (time.perf_counter() - self._start) * 1000
        for name, elapsed in self._use_case_timings:
            logger.info(f"{name} [{elapsed:.1f} ms]")
        logger.info(f"total [{total_elapsed:.1f} ms]")
        logger.info("Exit Domain")


class Domain(BaseDomain[Session]):
    pass
