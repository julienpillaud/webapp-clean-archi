from fastapi import status
from fastapi.testclient import TestClient

from tests.fixtures.factories.posts.base import PostBaseFactory


def test_search(post_factory: PostBaseFactory, client: TestClient) -> None:
    # Arrange
    number_of_posts = 2
    post_factory.create_many(3)
    title = "KeyWord In Title"
    search_term = "keyword"
    post_factory.create_many(number_of_posts, title=title)

    # Act
    response = client.get(f"/posts?search={search_term}")

    # Assert
    assert response.status_code == status.HTTP_200_OK
    result = response.json()
    assert result["total"] == number_of_posts
    assert len(result["items"]) == number_of_posts
    for item in result["items"]:
        assert (
            search_term in item["title"].lower()
            or search_term in item["content"].lower()
        )


def test_search_multiple_fields(
    post_factory: PostBaseFactory, client: TestClient
) -> None:
    # Arrange
    posts_with_title = 2
    title = "KeyWord In Title"
    post_factory.create_many(posts_with_title, title=title)

    posts_with_content = 3
    content = "KeyWord In Content"
    post_factory.create_many(posts_with_content, content=content)

    search_term = "keyword"

    # Act
    response = client.get(f"/posts?search={search_term}")

    # Assert
    assert response.status_code == status.HTTP_200_OK
    result = response.json()
    assert result["total"] == posts_with_title + posts_with_content
    assert len(result["items"]) == posts_with_title + posts_with_content
    for item in result["items"]:
        assert (
            search_term in item["title"].lower()
            or search_term in item["content"].lower()
        )


def test_search_no_results(post_factory: PostBaseFactory, client: TestClient) -> None:
    # Arrange
    post_factory.create_many(3)
    search_term = "nonexistent"

    # Act
    response = client.get(f"/posts?search={search_term}")

    # Assert
    assert response.status_code == status.HTTP_200_OK
    result = response.json()
    assert result["total"] == 0
    assert len(result["items"]) == 0
