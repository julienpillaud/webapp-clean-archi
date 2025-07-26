import uuid

from fastapi import status
from fastapi.testclient import TestClient

from app.domain.entities import DEFAULT_PAGINATION_LIMIT
from factories.posts.base import PostBaseFactory
from factories.users.base import UserBaseFactory


def test_get_users(user_factory: UserBaseFactory, client: TestClient) -> None:
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


def test_get_user(
    user_factory: UserBaseFactory,
    post_factory: PostBaseFactory,
    client: TestClient,
) -> None:
    # Arrange
    user = user_factory.create_one()
    posts = post_factory.create_many(3, author_id=user.id)

    # Act
    response = client.get(f"/users/{user.id}")

    # Assert
    assert response.status_code == status.HTTP_200_OK
    result = response.json()
    assert result["id"] == str(user.id)
    assert result["username"] == user.username
    assert result["email"] == user.email
    assert [post["id"] for post in result["posts"]] == [str(post.id) for post in posts]


def test_get_user_not_found(client: TestClient) -> None:
    # Act
    entity_id = uuid.uuid4()
    response = client.get(f"/users/{entity_id}")

    # Assert
    assert response.status_code == status.HTTP_404_NOT_FOUND
    result = response.json()
    assert result == {"detail": f"User '{entity_id}' not found."}


def test_create_user(client: TestClient) -> None:
    # Act
    data = {
        "email": "user@mail.com",
        "password": "password",
        "username": "User",
    }
    response = client.post("/users", json=data)

    # Assert
    assert response.status_code == status.HTTP_201_CREATED
    result = response.json()
    assert result["username"] == data["username"]
    assert result["email"] == data["email"]


def test_create_user_already_exists(
    client: TestClient, user_factory: UserBaseFactory
) -> None:
    # Arrange
    user = user_factory.create_one()

    # Act
    data = {
        "username": user.username,
        "password": "password",
        "email": user.email,
    }
    response = client.post("/users", json=data)

    # Assert
    assert response.status_code == status.HTTP_409_CONFLICT
    result = response.json()
    assert result == {"detail": f"User '{user.email}' already exists."}


def test_update_user(
    user_factory: UserBaseFactory,
    post_factory: PostBaseFactory,
    client: TestClient,
) -> None:
    # Arrange
    user = user_factory.create_one()
    posts = post_factory.create_many(3, author_id=user.id)

    # Act
    data = {"username": "User Updated"}
    response = client.patch(f"/users/{user.id}", json=data)

    # Assert
    assert response.status_code == status.HTTP_200_OK
    result = response.json()
    assert result["id"] == str(user.id)
    assert result["username"] == data["username"]
    assert result["email"] == user.email
    assert [post["id"] for post in result["posts"]] == [str(post.id) for post in posts]


def test_update_user_not_found(client: TestClient) -> None:
    # Act
    entity_id = uuid.uuid4()
    data = {"username": "User Updated"}
    response = client.patch(f"/users/{entity_id}", json=data)

    # Assert
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {"detail": f"User '{entity_id}' not found"}


def test_delete_user(user_factory: UserBaseFactory, client: TestClient) -> None:
    # Arrange
    user = user_factory.create_one()

    # Act
    response = client.delete(f"/users/{user.id}")

    # Assert
    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert response.content == b""

    response = client.get(f"/users/{user.id}")
    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_delete_user_not_found(client: TestClient) -> None:
    # Act
    entity_id = uuid.uuid4()
    response = client.delete(f"/users/{entity_id}")

    # Assert
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {"detail": f"User '{entity_id}' not found"}
