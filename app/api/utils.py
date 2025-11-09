from pydantic import BaseModel, NonNegativeInt

from app.domain.entities import Pagination


class BaseQuery(Pagination):
    search: str | None = None

    @property
    def pagination(self) -> Pagination:
        return Pagination(page=self.page, limit=self.limit)


class PaginatedResponseDTO[T: BaseModel](BaseModel):
    total: NonNegativeInt
    limit: NonNegativeInt
    items: list[T]
