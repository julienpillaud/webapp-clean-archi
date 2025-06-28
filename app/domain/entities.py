import uuid
from typing import Generic, TypeVar

from pydantic import BaseModel, ConfigDict, NonNegativeInt, PositiveInt

T = TypeVar("T", bound="DomainModel")

type EntityId = uuid.UUID | str


DEFAULT_PAGINATION_LIMIT = 10


class DomainModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: EntityId | None


class Token(BaseModel):
    access_token: str
    token_type: str


class Pagination(BaseModel):
    page: PositiveInt = 1
    limit: PositiveInt = DEFAULT_PAGINATION_LIMIT


class PaginatedResponse(BaseModel, Generic[T]):
    total: NonNegativeInt
    limit: NonNegativeInt
    items: list[T]
