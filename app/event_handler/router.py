from typing import Annotated, Any

import logfire
from faststream import Depends
from faststream.rabbit import RabbitRouter

from app.core.context import Context
from app.dependencies.faststream.dependencies import get_context

router = RabbitRouter()


@router.subscriber("item.event")
def handle_item_event(
    context: Annotated[Context, Depends(get_context)],
    message: Any,
) -> None:
    logfire.info(f"Sending event: {message}")
