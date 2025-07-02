from fastapi import status
from fastapi.testclient import TestClient


def test_protected_route(client: TestClient) -> None:
    response = client.get("/protected")
    assert response.status_code == status.HTTP_200_OK
