import uuid

from app.domain.context import ContextProtocol
from app.domain.items.entities import Item


def get_items(context: ContextProtocol, /) -> list[Item]:
    return context.item_repository.get_all().items


def create_item(context: ContextProtocol, /, name: str) -> None:
    context.item_repository.save(Item(id=uuid.uuid7(), name=name))


def create_item_then_fail(context: ContextProtocol, /, name: str) -> None:
    context.item_repository.save(Item(id=uuid.uuid4(), name=name))
    raise ValueError("boom")
