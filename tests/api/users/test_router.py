from fastapi import status
from fastapi.testclient import TestClient

from app.domain.entities import DEFAULT_PAGINATION_LIMIT
from tests.factories.users import UserFactory


def test_get_users(user_factory: UserFactory, client: TestClient) -> None:
    # Arrange
    number_of_user = 5
    user_factory.create_many(number_of_user)

    # Act
    response = client.get("/users")

    # Assert
    assert response.status_code == status.HTTP_200_OK
    result = response.json()
    assert result["total"] == number_of_user + 1  # first user for authentication
    assert result["limit"] == DEFAULT_PAGINATION_LIMIT
    assert len(result["items"]) == number_of_user + 1  # first user for authentication
