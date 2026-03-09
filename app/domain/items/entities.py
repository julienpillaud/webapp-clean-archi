from cleanstack.entities import DomainEntity, EntityId
from pydantic import BaseModel


class Item(DomainEntity):
    name: str


class ItemMessage(BaseModel):
    item_id: EntityId
    message: str
