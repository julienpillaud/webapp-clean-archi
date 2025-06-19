from app.core.context.sql import SqlContext
from app.domain.domain import TransactionalContextProtocol


def get_context() -> TransactionalContextProtocol:
    return SqlContext()
