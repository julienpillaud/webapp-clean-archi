from fastapi import status
from fastapi.testclient import TestClient

from tests.factories.posts import PostFactory


def test_pagination_request_less_than_total(
    post_factory: PostFactory, client: TestClient
) -> None:
    # Arrange
    total_number = 9
    request_number = 5
    post_factory.create_many(total_number)

    # Act
    response = client.get(f"/posts?page=1&limit={request_number}")

    # Assert
    assert response.status_code == status.HTTP_200_OK
    result = response.json()
    assert result["total"] == total_number
    assert result["limit"] == request_number
    assert len(result["items"]) == request_number


def test_pagination_request_more_than_total(
    post_factory: PostFactory, client: TestClient
) -> None:
    # Arrange
    total_number = 9
    request_number = 5
    post_factory.create_many(total_number)

    # Act
    response = client.get(f"/posts?page=2&limit={request_number}")

    # Assert
    assert response.status_code == status.HTTP_200_OK
    result = response.json()
    assert result["total"] == total_number
    assert result["limit"] == request_number
    assert len(result["items"]) == total_number - request_number


def test_pagination_out_of_range(post_factory: PostFactory, client: TestClient) -> None:
    # Arrange
    total_number = 9
    request_number = 5
    post_factory.create_many(total_number)

    # Act
    response = client.get(f"/posts?page=3&limit={request_number}")

    # Assert
    assert response.status_code == status.HTTP_200_OK
    result = response.json()
    assert result["total"] == total_number
    assert result["limit"] == request_number
    assert len(result["items"]) == 0
