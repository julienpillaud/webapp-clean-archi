import pytest
from fastapi import status
from fastapi.testclient import TestClient

from app.domain.filters import FilterOperator
from tests.factories.dummies import DummyFactory


def test_operator_eq(dummy_factory: DummyFactory, client: TestClient) -> None:
    count = 2
    dummy_factory.create_many(1, bool_field=True)
    dummy_factory.create_many(count, bool_field=False)

    params = {"filter": "bool_field=false"}
    response = client.get("/dummies", params=params)

    assert response.status_code == status.HTTP_200_OK
    result = response.json()
    assert len(result["items"]) == count


@pytest.mark.parametrize(
    "operator",
    (
        FilterOperator.LT,
        FilterOperator.LTE,
        FilterOperator.GTE,
        FilterOperator.GT,
    ),
)
def test_unsupported_operator(client: TestClient, operator: FilterOperator) -> None:
    params = {"filter": f"bool_field[{operator}]=false"}
    response = client.get("/dummies", params=params)

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT
    result = response.json()
    assert result == {"detail": "Unsupported operator."}


def test_wrong_value(client: TestClient) -> None:
    params = {"filter": "bool_field=bad"}
    response = client.get("/dummies", params=params)

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT
    result = response.json()
    assert result == {"detail": "Invalid value format."}
