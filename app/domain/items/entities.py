from pydantic import BaseModel

from app.domain.entities import DomainEntity, EntityId


class Item(DomainEntity):
    name: str


class ItemMessage(BaseModel):
    item_id: EntityId
    message: str
