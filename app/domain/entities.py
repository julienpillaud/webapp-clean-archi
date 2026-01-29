import uuid

from pydantic import BaseModel, ConfigDict, NonNegativeInt, PositiveInt

type EntityId = uuid.UUID

DEFAULT_PAGINATION_LIMIT = 10


class DomainEntity(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: EntityId


class Token(BaseModel):
    access_token: str
    token_type: str


class Pagination(BaseModel):
    page: PositiveInt = 1
    limit: PositiveInt = DEFAULT_PAGINATION_LIMIT

    @property
    def skip(self) -> int:
        return (self.page - 1) * self.limit


class PaginatedResponse[T: DomainEntity](BaseModel):
    total: NonNegativeInt
    limit: NonNegativeInt
    items: list[T]
