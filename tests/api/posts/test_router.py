import uuid

from fastapi import status
from fastapi.testclient import TestClient

from app.domain.entities import DEFAULT_PAGINATION_LIMIT
from tests.fixtures.factories import PostFactory, UserFactory


def test_get_posts(post_factory: PostFactory, client: TestClient):
    # Arrange
    number_of_post = 5
    post_factory.create_many(number_of_post)

    # Act
    response = client.get("/posts")

    # Assert
    assert response.status_code == status.HTTP_200_OK
    result = response.json()
    assert result["total"] == number_of_post
    assert result["limit"] == DEFAULT_PAGINATION_LIMIT
    assert len(result["items"]) == number_of_post


def test_get_post(post_factory: PostFactory, client: TestClient):
    # Arrange
    post = post_factory.create_one()

    # Act
    response = client.get(f"/posts/{post.id}")

    # Assert
    assert response.status_code == status.HTTP_200_OK
    result = response.json()
    assert result["id"] == str(post.id)
    assert result["title"] == post.title
    assert result["content"] == post.content
    assert result["author_id"] == str(post.author_id)
    assert result["tags"] == post.tags


def test_get_post_not_found(client: TestClient):
    # Act
    fake_id = uuid.uuid4()
    response = client.get(f"/posts/{fake_id}")

    # Assert
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {"detail": f"Post '{fake_id}' not found"}


def test_create_post(user_factory: UserFactory, client: TestClient):
    # Arrange
    user = user_factory.create_one()

    # Act
    data = {
        "title": "Post",
        "content": "Post content",
        "author_id": str(user.id),
        "tags": ["python", "fastapi"],
    }
    response = client.post("/posts", json=data)

    # Assert
    assert response.status_code == status.HTTP_201_CREATED
    result = response.json()
    assert result["title"] == data["title"]
    assert result["content"] == data["content"]
    assert result["author_id"] == data["author_id"]
    assert result["tags"] == data["tags"]


def test_create_post_user_not_found(client: TestClient):
    # Act
    data = {
        "title": "Post",
        "content": "Post content",
        "author_id": str(uuid.uuid4()),
        "tags": ["python", "fastapi"],
    }
    response = client.post("/posts", json=data)

    # Assert
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {"detail": f"User '{data['author_id']}' not found."}


def test_update_post(post_factory: PostFactory, client: TestClient):
    # Arrange
    post = post_factory.create_one()

    # Act
    data = {"title": "Post Updated"}
    response = client.patch(f"/posts/{post.id}", json=data)

    # Assert
    assert response.status_code == status.HTTP_200_OK
    result = response.json()
    assert result["id"] == str(post.id)
    assert result["title"] == data["title"]
    assert result["content"] == post.content
    assert result["author_id"] == str(post.author_id)
    assert result["tags"] == post.tags


def test_update_post_not_found(client: TestClient):
    # Act
    fake_id = uuid.uuid4()
    data = {"title": "Post Updated"}
    response = client.patch(f"/posts/{fake_id}", json=data)

    # Assert
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {"detail": f"Post '{fake_id}' not found"}


def test_delete_post(post_factory: PostFactory, client: TestClient):
    # Arrange
    post = post_factory.create_one()

    # Act
    response = client.delete(f"/posts/{post.id}")

    # Assert
    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert response.content == b""


def test_delete_post_not_found(client: TestClient):
    # Act
    fake_id = uuid.uuid4()
    response = client.delete(f"/posts/{fake_id}")

    # Assert
    assert response.status_code == status.HTTP_404_NOT_FOUND
    result = response.json()
    assert result == {"detail": f"Post '{fake_id}' not found."}
