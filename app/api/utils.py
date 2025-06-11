from typing import Generic, TypeVar

from pydantic import BaseModel, NonNegativeInt

from app.domain.entities import Pagination

T = TypeVar("T", bound=BaseModel)


class FilterParams(Pagination):
    search: str | None = None

    def to_pagination(self) -> Pagination:
        return Pagination(page=self.page, limit=self.limit)


class PaginatedResponseDTO(BaseModel, Generic[T]):
    total: NonNegativeInt
    limit: NonNegativeInt
    items: list[T]
