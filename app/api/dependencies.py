from typing import Annotated

from fastapi import Depends

from app.core.context.utils import get_context
from app.domain.domain import Domain, TransactionalContextProtocol


def get_domain(
    context: Annotated[TransactionalContextProtocol, Depends(get_context)],
) -> Domain:
    return Domain(context=context)
