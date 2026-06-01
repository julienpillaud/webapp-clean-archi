import uuid

from cleanstack.entities import DEFAULT_PAGINATION_SIZE
from fastapi import status
from fastapi.testclient import TestClient

from tests.plugins.factories import Factory


def test_get_posts(factory: Factory, client: TestClient) -> None:
    # Arrange
    posts_count = 5
    factory.posts.create_many(posts_count)

    # Act
    response = client.get("/posts")

    # Assert
    assert response.status_code == status.HTTP_200_OK
    result = response.json()
    assert result["total"] == posts_count
    assert result["size"] == DEFAULT_PAGINATION_SIZE
    assert len(result["items"]) == posts_count


def test_get_post(factory: Factory, client: TestClient) -> None:
    # Arrange
    post = factory.posts.create_one()

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


def test_get_post_not_found(client: TestClient) -> None:
    # Act
    entity_id = uuid.uuid7()
    response = client.get(f"/posts/{entity_id}")

    # Assert
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {"detail": f"Post '{entity_id}' not found"}


def test_create_post(factory: Factory, client: TestClient) -> None:
    # Arrange
    user = factory.users.create_one()

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


def test_create_post_user_not_found(client: TestClient) -> None:
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


def test_update_post(factory: Factory, client: TestClient) -> None:
    # Arrange
    post = factory.posts.create_one()

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


def test_update_post_add_tag(factory: Factory, client: TestClient) -> None:
    # Arrange
    post = factory.posts.create_one()

    # Act
    data = {"tags": [*post.tags, "new_tag"]}
    response = client.patch(f"/posts/{post.id}", json=data)

    # Assert
    assert response.status_code == status.HTTP_200_OK
    result = response.json()
    assert result["tags"] == data["tags"]


def test_update_post_replace_tags(factory: Factory, client: TestClient) -> None:
    # Arrange
    post = factory.posts.create_one()

    # Act
    data = {"tags": ["new_tag1", "new_tag2"]}
    response = client.patch(f"/posts/{post.id}", json=data)

    # Assert
    assert response.status_code == status.HTTP_200_OK
    result = response.json()
    assert result["tags"] == data["tags"]


def test_update_post_remove_tag(factory: Factory, client: TestClient) -> None:
    # Arrange
    post = factory.posts.create_one(tags=["Python", "FastAPI"])

    # Act
    data = {"tags": post.tags[:-1]}  # Remove last tag
    response = client.patch(f"/posts/{post.id}", json=data)

    # Assert
    assert response.status_code == status.HTTP_200_OK
    result = response.json()
    assert result["tags"] == data["tags"]


def test_update_post_remove_all_tags(factory: Factory, client: TestClient) -> None:
    # Arrange
    post = factory.posts.create_one()

    # Act
    data: dict[str, list[str]] = {"tags": []}  # Remove all tags
    response = client.patch(f"/posts/{post.id}", json=data)

    # Assert
    assert response.status_code == status.HTTP_200_OK
    result = response.json()
    assert result["tags"] == data["tags"]


def test_update_post_not_found(client: TestClient) -> None:
    # Act
    entity_id = uuid.uuid4()
    data = {"title": "Post Updated"}
    response = client.patch(f"/posts/{entity_id}", json=data)

    # Assert
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {"detail": f"Post '{entity_id}' not found"}


def test_delete_post(factory: Factory, client: TestClient) -> None:
    # Arrange
    post = factory.posts.create_one()

    # Act
    response = client.delete(f"/posts/{post.id}")

    # Assert
    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert response.content == b""

    response = client.get(f"/posts/{post.id}")
    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_delete_post_not_found(client: TestClient) -> None:
    # Act
    entity_id = uuid.uuid7()
    response = client.delete(f"/posts/{entity_id}")

    # Assert
    assert response.status_code == status.HTTP_404_NOT_FOUND
    result = response.json()
    assert result == {"detail": f"Post '{entity_id}' not found."}
