import uuid
from typing import Generic, NewType, TypeVar

from pydantic import BaseModel, ConfigDict, NonNegativeInt, PositiveInt

T = TypeVar("T", bound="DomainModel")

TagName = NewType("TagName", str)

DEFAULT_PAGINATION_LIMIT = 10


class DomainModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID


class Pagination(BaseModel):
    page: PositiveInt = 1
    limit: PositiveInt = DEFAULT_PAGINATION_LIMIT


class PaginatedResponse(BaseModel, Generic[T]):
    total: NonNegativeInt
    limit: NonNegativeInt
    items: list[T]
