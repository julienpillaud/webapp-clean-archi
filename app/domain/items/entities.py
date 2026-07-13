from cleanstack import BaseEntity
from pydantic import BaseModel


class Item(BaseEntity):
    name: str


class ItemCreate(BaseModel):
    name: str
