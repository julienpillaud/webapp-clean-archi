from typing import Generic, TypeVar

from pydantic import BaseModel, NonNegativeInt

from app.domain.entities import Pagination

T = TypeVar("T", bound=BaseModel)


class BaseQuery(Pagination):
    search: str | None = None

    @property
    def pagination(self) -> Pagination:
        return Pagination(page=self.page, limit=self.limit)


class PaginatedResponseDTO(BaseModel, Generic[T]):
    total: NonNegativeInt
    limit: NonNegativeInt
    items: list[T]
