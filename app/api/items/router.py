from typing import Annotated

from fastapi import APIRouter, Depends

from app.api.dependencies import get_domain
from app.core.domain import Domain
from app.domain.items.entities import Item, ItemCreate
from app.domain.items.use_cases import (
    create_item,
    create_item_then_fail,
    get_items,
)

router = APIRouter(prefix="/items", tags=["items"])


@router.get("")
def get_items_endpoint(domain: Annotated[Domain, Depends(get_domain)]) -> list[Item]:
    return domain.query(get_items)


@router.post("/via-command")
def create_item_via_command_endpoint(
    domain: Annotated[Domain, Depends(get_domain)],
    data: ItemCreate,
) -> None:
    domain.command(create_item, name=data.name)


@router.post("/via-query")
def create_item_via_query_endpoint(
    domain: Annotated[Domain, Depends(get_domain)],
    data: ItemCreate,
) -> None:
    domain.query(create_item, name=data.name)


@router.post("/create-then-fail")
def create_item_then_fail_endpoint(
    domain: Annotated[Domain, Depends(get_domain)],
    data: ItemCreate,
) -> None:
    domain.command(create_item_then_fail, name=data.name)


@router.post("/command-then-query")
def create_item_command_then_query_endpoint(
    domain: Annotated[Domain, Depends(get_domain)],
    data: ItemCreate,
) -> None:
    domain.command(create_item, name=data.name)
    domain.query(create_item, name="ignored")
