import logging
import time
from collections.abc import Iterator
from contextlib import contextmanager
from typing import Any, Self

from pydantic import BaseModel
from sqlalchemy import Connection, Engine, event
from sqlalchemy.engine.interfaces import DBAPICursor, ExecutionContext

logger = logging.getLogger(__name__)


class QueryInfo(BaseModel):
    statement: str
    parameters: dict[str, Any]
    duration: float


class SQLAlchemyInstrument:
    queries: list[QueryInfo]

    def __init__(self) -> None:
        raise RuntimeError("Use SQLAlchemyInstrument.record() to instantiate.")

    @property
    def queries_count(self) -> int:
        return len(self.queries)

    @property
    def total_duration(self) -> float:
        return sum(query.duration for query in self.queries)

    @classmethod
    @contextmanager
    def record(cls) -> Iterator[Self]:
        instance = object.__new__(cls)
        instance.queries = []
        instance._setup_listeners()

        try:
            yield instance
        finally:
            instance._remove_listeners()

    def _setup_listeners(self) -> None:
        event.listen(
            Engine,
            "before_cursor_execute",
            self._before_cursor_execute,
        )
        event.listen(
            Engine,
            "after_cursor_execute",
            self._after_cursor_execute,
        )

    def _remove_listeners(self) -> None:
        if event.contains(
            Engine,
            "before_cursor_execute",
            self._before_cursor_execute,
        ):
            event.remove(
                Engine,
                "before_cursor_execute",
                self._before_cursor_execute,
            )
        if event.contains(
            Engine,
            "after_cursor_execute",
            self._after_cursor_execute,
        ):
            event.remove(
                Engine,
                "after_cursor_execute",
                self._after_cursor_execute,
            )

    def _before_cursor_execute(
        self,
        conn: Connection,
        cursor: DBAPICursor,
        statement: str,
        parameters: dict[str, Any],
        context: ExecutionContext,
        executemany: bool,
    ) -> None:
        conn.info["start_time"] = time.perf_counter()

    def _after_cursor_execute(
        self,
        conn: Connection,
        cursor: DBAPICursor,
        statement: str,
        parameters: dict[str, Any],
        context: ExecutionContext,
        executemany: bool,
    ) -> None:
        start_time = conn.info.get("start_time")
        duration = (time.perf_counter() - start_time) * 1000 if start_time else 0
        statement = statement.replace("\n", " ").strip()
        logger.info(f"[{duration or '':6.2f} ms] {statement}")

        query_info = QueryInfo(
            statement=statement,
            parameters=parameters,
            duration=duration,
        )
        self.queries.append(query_info)
