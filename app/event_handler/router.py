from typing import Annotated, Any

import logfire
from faststream import Depends
from faststream.rabbit import RabbitRouter

from app.dependencies.faststream.dependencies import get_domain
from app.domain.domain import Domain

router = RabbitRouter()


@router.subscriber("item.event")
def handle_item_event(
    domain: Annotated[Domain, Depends(get_domain)],
    message: Any,
) -> None:
    logfire.info(f"Sending event: {message}")
