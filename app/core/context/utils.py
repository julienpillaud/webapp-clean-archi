from app.core.context.sql import SqlContext
from app.domain.domain import TransactionalContextProtocol


def get_context() -> TransactionalContextProtocol:
    global _sql_context_instance
    if _sql_context_instance is None:
        _sql_context_instance = SqlContext()
    return _sql_context_instance


_sql_context_instance = None
