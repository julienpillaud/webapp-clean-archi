import uuid

from pydantic import BaseModel, NonNegativeInt, PositiveInt

type EntityId = uuid.UUID

DEFAULT_PAGINATION_LIMIT = 10


class DomainEntity(BaseModel):
    id: EntityId


class Token(BaseModel):
    access_token: str
    token_type: str


class Pagination(BaseModel):
    page: PositiveInt = 1
    limit: PositiveInt = DEFAULT_PAGINATION_LIMIT


class PaginatedResponse[T: DomainEntity](BaseModel):
    total: NonNegativeInt
    limit: NonNegativeInt
    items: list[T]
