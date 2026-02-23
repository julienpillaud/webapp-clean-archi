import pytest
from fastapi import status
from fastapi.testclient import TestClient
from pytest import FixtureRequest

from app.domain.entities import DEFAULT_PAGINATION_LIMIT


@pytest.mark.parametrize(
    "factory_name, repo_type",
    [
        ("item_mongo_factory", "document"),
        ("item_sql_factory", "relational"),
    ],
)
def test_get_items(
    client: TestClient,
    factory_name: str,
    repo_type: str,
    request: FixtureRequest,
) -> None:
    factory = request.getfixturevalue(factory_name)
    number_of_items = 5
    factory.create_many(number_of_items)

    # Act
    response = client.get(f"/items?repository={repo_type}")

    # Assert
    assert response.status_code == status.HTTP_200_OK
    result = response.json()
    assert result["total"] == number_of_items
    assert result["limit"] == DEFAULT_PAGINATION_LIMIT
    assert len(result["items"]) == number_of_items


def test_send_item_event(client: TestClient) -> None:
    response = client.post("/items/event")

    assert response.status_code == status.HTTP_200_OK
