from typing import Annotated, Any

from fastapi import APIRouter, Depends

from app.api.dummies.dtos import DummyDTO
from app.api.utils import PaginatedResponseDTO
from app.dependencies.fastapi.dependencies import (
    get_current_user,
    get_domain,
    get_filters,
)
from app.domain.domain import Domain
from app.domain.entities import Pagination
from app.domain.filters import FilterEntity

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
    search: str | None = None,
) -> Any:
    return domain.get_dummies(pagination=pagination, search=search, filters=filters)


@router.get(
    "/cached",
    response_model=PaginatedResponseDTO[DummyDTO],
    dependencies=[Depends(get_current_user)],
)
def get_dummies_cached(
    domain: Annotated[Domain, Depends(get_domain)],
    pagination: Annotated[Pagination, Depends()],
    filters: Annotated[list[FilterEntity], Depends(get_filters)],
    search: str | None = None,
) -> Any:
    return domain.get_dummies_cached(
        pagination=pagination, search=search, filters=filters
    )
