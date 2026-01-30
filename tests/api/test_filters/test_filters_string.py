import pytest
from fastapi import status
from fastapi.testclient import TestClient

from app.domain.filters import FilterOperator
from tests.factories.dummies import DummyFactory


def test_operator_eq(dummy_factory: DummyFactory, client: TestClient) -> None:
    count = 2
    field = "included"
    dummy_factory.create_one(string_field="excluded")
    dummy_factory.create_many(count, string_field=field)

    params = {"filter": f"string_field={field}"}
    response = client.get("/dummies", params=params)

    assert response.status_code == status.HTTP_200_OK
    result = response.json()
    assert len(result["items"]) == count


def test_operator_in(dummy_factory: DummyFactory, client: TestClient) -> None:
    count = 2
    fields = ("included1", "included2")
    dummy_factory.create_one(string_field="excluded")
    dummy_factory.create_one(string_field=fields[0])
    dummy_factory.create_one(string_field=fields[1])

    params = {"filter": f"string_field[in]={','.join(fields)}"}
    response = client.get("/dummies", params=params)

    assert response.status_code == status.HTTP_200_OK
    result = response.json()
    assert len(result["items"]) == count


def test_operator_not_in(dummy_factory: DummyFactory, client: TestClient) -> None:
    count = 1
    fields = ("excluded1", "excluded2")
    dummy_factory.create_one(string_field="excluded1")
    dummy_factory.create_one(string_field="excluded2")
    dummy_factory.create_one(string_field="included")

    params = {"filter": f"string_field[nin]={','.join(fields)}"}
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
def test_unsupported_operator(
    client: TestClient,
    operator: FilterOperator,
) -> None:
    params = {"filter": f"string_field[{operator}]=test"}
    response = client.get("/dummies", params=params)

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT
    result = response.json()
    assert result == {"detail": "Unsupported operator."}
