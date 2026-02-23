from typing import Annotated

import logfire
from faststream import Depends
from faststream.rabbit import RabbitRouter

from app.domain.domain import Domain
from app.domain.items.entities import ItemMessage
from app.event_handler.dependencies import get_domain

router = RabbitRouter()


@router.subscriber("item.event")
def handle_item_event(
    domain: Annotated[Domain, Depends(get_domain)],
    message: ItemMessage,
) -> None:
    logfire.info(f"Sending event: {message}")
    domain.handle_item_event(message=message)
