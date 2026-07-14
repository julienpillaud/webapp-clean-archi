import uuid

from app.domain.context import ContextProtocol
from app.domain.items.entities import Item


def get_items(context: ContextProtocol, /) -> list[Item]:
    return context.item_repository.get_all().items


def create_item(context: ContextProtocol, /, name: str) -> Item:
    item = Item(id=uuid.uuid7(), name=name)
    context.item_repository.save(item)
    return item
