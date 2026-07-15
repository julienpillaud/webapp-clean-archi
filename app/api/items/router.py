from typing import Annotated

from fastapi import APIRouter, Depends, status

from app.api.dependencies import get_domain
from app.core.domain.synchronous import Domain
from app.domain.items.entities import Item, ItemCreate
from app.domain.items.use_cases import create_item, get_items

router = APIRouter(prefix="/items", tags=["items"])


@router.get("")
def get_items_endpoint(
    domain: Annotated[Domain, Depends(get_domain)],
) -> list[Item]:
    return domain.run(get_items)


@router.post("", status_code=status.HTTP_201_CREATED)
def create_item_endpoint(
    domain: Annotated[Domain, Depends(get_domain)],
    data: ItemCreate,
) -> Item:
    return domain.run(create_item, name=data.name)
