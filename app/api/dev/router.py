from typing import Annotated

from fastapi import APIRouter, Depends

from app.dependencies.fastapi.dependencies import get_domain
from app.domain.domain import Domain

router = APIRouter(tags=["dev"])


@router.get("/benchmark")
def benchmark(domain: Annotated[Domain, Depends(get_domain)]) -> str:
    return domain.benchmark()


@router.get("/custom-error")
def simulate_custom_error(
    domain: Annotated[Domain, Depends(get_domain)],
) -> None:
    domain.custom_error()


@router.get("/unexpected-error")
def simulate_unexpected_error(
    domain: Annotated[Domain, Depends(get_domain)],
) -> None:
    domain.unexpected_error()


@router.get("/unexpected-domain-error")
def simulate_unexpected_domain_error(
    domain: Annotated[Domain, Depends(get_domain)],
) -> None:
    domain.unexpected_domain_error()
