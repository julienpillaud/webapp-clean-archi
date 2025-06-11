from fastapi import status
from fastapi.testclient import TestClient

from tests.fixtures.factories.posts.base import PostBaseFactory


def test_search(post_factory: PostBaseFactory, client: TestClient) -> None:
    # Arrange
    number_of_post = 2
    post_factory.create_many(3)
    search_term = "keyword"
    post_factory.create_many(number_of_post, title=f"{search_term}title")

    # Act
    response = client.get(f"/posts?search={search_term}")

    # Assert
    assert response.status_code == status.HTTP_200_OK
    result = response.json()
    assert result["total"] == number_of_post
    assert len(result["items"]) == number_of_post
    for item in result["items"]:
        assert search_term in item["title"] or search_term in item["content"]
