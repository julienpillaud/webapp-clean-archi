import uuid

from fastapi import status
from fastapi.testclient import TestClient

from app.domain.entities import DEFAULT_PAGINATION_LIMIT
from tests.fixtures.factories import UserFactory


def test_get_users(user_factory: UserFactory, client: TestClient):
    # Arrange
    number_of_user = 5
    user_factory.create_many(number_of_user)

    # Act
    response = client.get("/users")

    # Assert
    assert response.status_code == status.HTTP_200_OK
    result = response.json()
    assert result["total"] == number_of_user
    assert result["limit"] == DEFAULT_PAGINATION_LIMIT
    assert len(result["items"]) == number_of_user


def test_get_user(user_factory: UserFactory, client: TestClient):
    # Arrange
    user = user_factory.create_one()

    # Act
    response = client.get(f"/users/{user.id}")

    # Assert
    assert response.status_code == status.HTTP_200_OK
    result = response.json()
    assert result["id"] == str(user.id)
    assert result["username"] == user.username
    assert result["email"] == user.email


def test_get_user_not_found(client: TestClient):
    # Act
    fake_id = uuid.uuid4()
    response = client.get(f"/users/{fake_id}")

    # Assert
    assert response.status_code == status.HTTP_404_NOT_FOUND
    result = response.json()
    assert result == {"detail": f"User '{fake_id}' not found."}


def test_create_user(client: TestClient):
    # Act
    data = {"username": "User", "email": "user@mail.com"}
    response = client.post("/users", json=data)

    # Assert
    assert response.status_code == status.HTTP_201_CREATED
    result = response.json()
    assert result["username"] == data["username"]
    assert result["email"] == data["email"]


def test_create_user_already_exists(client: TestClient, user_factory: UserFactory):
    # Arrange
    user = user_factory.create_one()

    # Act
    data = {"username": user.username, "email": user.email}
    response = client.post("/users", json=data)

    # Assert
    assert response.status_code == status.HTTP_409_CONFLICT
    result = response.json()
    assert result == {"detail": f"User '{user.email}' already exists."}


def test_update_user(user_factory: UserFactory, client: TestClient):
    # Arrange
    user = user_factory.create_one()

    # Act
    data = {"username": "User Updated"}
    response = client.patch(f"/users/{user.id}", json=data)

    # Assert
    assert response.status_code == status.HTTP_200_OK
    result = response.json()
    assert result["id"] == str(user.id)
    assert result["username"] == data["username"]
    assert result["email"] == user.email


def test_update_user_not_found(client: TestClient):
    # Act
    fake_id = uuid.uuid4()
    data = {"username": "User Updated"}
    response = client.patch(f"/users/{fake_id}", json=data)

    # Assert
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {"detail": f"User '{fake_id}' not found"}


def test_delete_user(user_factory: UserFactory, client: TestClient):
    # Arrange
    user = user_factory.create_one()

    # Act
    response = client.delete(f"/users/{user.id}")

    # Assert
    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert response.content == b""


def test_delete_user_not_found(client: TestClient):
    # Act
    fake_id = uuid.uuid4()
    response = client.delete(f"/users/{fake_id}")

    # Assert
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {"detail": f"User '{fake_id}' not found"}
