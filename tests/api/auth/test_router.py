from fastapi import status
from fastapi.testclient import TestClient

from factories.users import UserFactory


def test_get_access_token(user_factory: UserFactory, client: TestClient) -> None:
    # Arrange
    password = "password"
    user = user_factory.create_one(password=password, hash_password=True)

    # Act
    data = {"username": user.email, "password": password}
    response = client.post("/auth/access-token", data=data)

    # Assert
    assert response.status_code == status.HTTP_200_OK
    result = response.json()
    assert result["access_token"].startswith("eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9")
    assert result["token_type"] == "bearer"


def test_get_access_token_invalid_username(
    user_factory: UserFactory, client: TestClient
) -> None:
    # Arrange
    password = "password"
    user_factory.create_one(password=password)

    # Act
    data = {"username": "invalid", "password": password}
    response = client.post("/auth/access-token", data=data)

    # Assert
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    result = response.json()
    assert result["detail"] == "Incorrect username or password."


def test_get_access_token_invalid_password(
    user_factory: UserFactory, client: TestClient
) -> None:
    # Arrange
    password = "password"
    user = user_factory.create_one(password=password, hash_password=True)

    # Act
    data = {"username": user.email, "password": "invalid"}
    response = client.post("/auth/access-token", data=data)

    # Assert
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    result = response.json()
    assert result["detail"] == "Incorrect username or password."
