import uuid

import pytest
from starlette import status
from starlette.testclient import TestClient

from app.domain.filters import FilterOperator
from tests.factories.dummies import DummyFactory


def test_operator_eq(dummy_factory: DummyFactory, client: TestClient) -> None:
    count = 2
    field = uuid.uuid7()
    dummy_factory.create_one()
    dummy_factory.create_many(count, uuid_field=field)

    params = {"filter": f"uuid_field={field}"}
    response = client.get("/dummies", params=params)

    assert response.status_code == status.HTTP_200_OK
    result = response.json()
    assert len(result["items"]) == count


def test_operator_in(dummy_factory: DummyFactory, client: TestClient) -> None:
    count = 2
    fields = (uuid.uuid7(), uuid.uuid7())
    dummy_factory.create_one()
    dummy_factory.create_one(uuid_field=fields[0])
    dummy_factory.create_one(uuid_field=fields[1])

    params = {"filter": f"uuid_field[in]={fields[0]},{fields[1]}"}
    response = client.get("/dummies", params=params)

    assert response.status_code == status.HTTP_200_OK
    result = response.json()
    assert len(result["items"]) == count


def test_operator_not_in(dummy_factory: DummyFactory, client: TestClient) -> None:
    count = 1
    fields = (uuid.uuid7(), uuid.uuid7())
    dummy_factory.create_one()
    dummy_factory.create_one(uuid_field=fields[0])
    dummy_factory.create_one(uuid_field=fields[1])

    params = {"filter": f"uuid_field[nin]={fields[0]},{fields[1]}"}
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
    params = {"filter": f"uuid_field[{operator}]=test"}
    response = client.get("/dummies", params=params)

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT
    result = response.json()
    assert result == {"detail": "Unsupported operator."}


def test_wrong_value(client: TestClient) -> None:
    params = {"filter": "uuid_field=bad"}
    response = client.get("/dummies", params=params)

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT
    result = response.json()
    assert result == {"detail": "Invalid value format."}
