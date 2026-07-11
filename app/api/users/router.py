from typing import Annotated

from cleanstack import PaginatedResponse
from cleanstack.entities import FilterEntity, Pagination, SortEntity
from fastapi import APIRouter, Depends

from app.api.dependencies import get_domain, get_filters, get_sort_entities
from app.core.domain import Domain
from app.domain.users.entities import User
from app.domain.users.use_cases import get_users

router = APIRouter(prefix="/users", tags=["users"])


@router.get("")
def get_users_endpoint(
    domain: Annotated[Domain, Depends(get_domain)],
    pagination: Annotated[Pagination, Depends()],
    filters: Annotated[list[FilterEntity], Depends(get_filters)],
    sort: Annotated[list[SortEntity], Depends(get_sort_entities)],
    search: str | None = None,
) -> PaginatedResponse[User]:
    return domain.query(
        get_users,
        search=search,
        filters=filters,
        sort=sort,
        pagination=pagination,
    )
