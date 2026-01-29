import datetime

import pytest
from fastapi import status
from fastapi.testclient import TestClient

from app.domain.filters import FilterOperator
from tests.factories.dummies import DummyFactory


@pytest.mark.parametrize(
    "operator, expected_count",
    [
        (FilterOperator.LT, 1),  # 2025-12-31
        (FilterOperator.LTE, 3),  # 2025-12-31 + 2026-01-01
        (FilterOperator.EQ, 2),  # 2026-01-01
        (FilterOperator.GT, 4),  # 2026-02-01
        (FilterOperator.GTE, 6),  # 2026-01-01 + 2026-02-01
    ],
)
def test_comparison_operators(
    dummy_factory: DummyFactory,
    client: TestClient,
    operator: FilterOperator,
    expected_count: int,
) -> None:
    past_date = datetime.date(2025, 12, 31)
    target_date = datetime.date(2026, 1, 1)
    future_date = datetime.date(2026, 2, 1)

    dummy_factory.create_many(1, date_field=past_date)
    dummy_factory.create_many(2, date_field=target_date)
    dummy_factory.create_many(4, date_field=future_date)

    op_suffix = f"[{operator}]" if operator != FilterOperator.EQ else ""
    params = {"filter": f"date_field{op_suffix}={target_date.isoformat()}"}
    response = client.get("/dummies", params=params)

    assert response.status_code == status.HTTP_200_OK
    result = response.json()
    assert len(result["items"]) == expected_count


def test_operator_in(dummy_factory: DummyFactory, client: TestClient) -> None:
    count = 2
    date_a = datetime.date(2026, 1, 1)
    date_b = datetime.date(2026, 2, 2)
    date_c = datetime.date(2026, 3, 3)

    dummy_factory.create_one(date_field=date_a)
    dummy_factory.create_one(date_field=date_b)
    dummy_factory.create_one(date_field=date_c)

    params = {"filter": f"date_field[in]={date_a.isoformat()},{date_b.isoformat()}"}
    response = client.get("/dummies", params=params)

    assert response.status_code == status.HTTP_200_OK
    result = response.json()
    assert len(result["items"]) == count


def test_operator_nin(dummy_factory: DummyFactory, client: TestClient) -> None:
    count = 1
    date_a = datetime.date(2026, 1, 1)
    date_b = datetime.date(2026, 2, 2)
    date_c = datetime.date(2026, 3, 3)

    dummy_factory.create_one(date_field=date_a)
    dummy_factory.create_one(date_field=date_b)
    dummy_factory.create_one(date_field=date_c)

    params = {"filter": f"date_field[nin]={date_a.isoformat()},{date_b.isoformat()}"}
    response = client.get("/dummies", params=params)

    assert response.status_code == status.HTTP_200_OK
    result = response.json()
    assert len(result["items"]) == count
    assert result["items"][0]["date_field"] == date_c.isoformat()


def test_wrong_value(client: TestClient) -> None:
    params = {"filter": "date_field=bad"}
    response = client.get("/dummies", params=params)

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT
    result = response.json()
    assert result == {"detail": "Invalid value format."}
