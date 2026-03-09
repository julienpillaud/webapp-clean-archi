from typing import Annotated, Any

from cleanstack.entities import FilterEntity, Pagination, SortEntity
from fastapi import APIRouter, Depends

from app.api.dummies.dtos import DummyDTO
from app.api.utils import PaginatedResponseDTO
from app.dependencies.fastapi.dependencies import (
    get_current_user,
    get_domain,
    get_filters,
    get_sort_entities,
)
from app.domain.domain import Domain

router = APIRouter(prefix="/dummies", tags=["dummies"])


@router.get(
    "",
    response_model=PaginatedResponseDTO[DummyDTO],
    dependencies=[Depends(get_current_user)],
)
def get_dummies(
    domain: Annotated[Domain, Depends(get_domain)],
    pagination: Annotated[Pagination, Depends()],
    filters: Annotated[list[FilterEntity], Depends(get_filters)],
    sort: Annotated[list[SortEntity], Depends(get_sort_entities)],
    search: str | None = None,
) -> Any:
    return domain.get_dummies(
        search=search,
        filters=filters,
        sort=sort,
        pagination=pagination,
    )


@router.get(
    "/cached",
    response_model=PaginatedResponseDTO[DummyDTO],
    dependencies=[Depends(get_current_user)],
)
def get_dummies_cached(
    domain: Annotated[Domain, Depends(get_domain)],
    pagination: Annotated[Pagination, Depends()],
    filters: Annotated[list[FilterEntity], Depends(get_filters)],
    sort: Annotated[list[SortEntity], Depends(get_sort_entities)],
    search: str | None = None,
) -> Any:
    return domain.get_dummies_cached(
        search=search,
        filters=filters,
        sort=sort,
        pagination=pagination,
    )
