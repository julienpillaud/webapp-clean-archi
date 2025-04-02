from typing import Generic, TypeVar

from pydantic import BaseModel, NonNegativeInt

from app.domain.entities import Pagination

T = TypeVar("T", bound=BaseModel)


class PaginationDTO(Pagination):
    def to_domain(self) -> Pagination:
        return Pagination.model_validate(self)


class PaginatedResponseDTO(BaseModel, Generic[T]):
    total: NonNegativeInt
    limit: NonNegativeInt
    items: list[T]
