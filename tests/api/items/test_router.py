import pytest
from fastapi.testclient import TestClient


def test_create_item_via_command_persists(client: TestClient) -> None:
    client.post("/items/via-command", json={"name": "A"})

    response = client.get("/items")
    assert len(response.json()) == 1


def test_create_item_via_query_never_persists(client: TestClient) -> None:
    client.post("/items/via-query", json={"name": "A"})

    response = client.get("/items")
    assert response.json() == []


def test_command_failure_rolls_back(client: TestClient) -> None:
    with pytest.raises(ValueError):
        client.post("/items/create-then-fail", json={"name": "Ghost"})

    response = client.get("/items")
    assert response.json() == []


def test_mutation_flag_never_downgrades(client: TestClient) -> None:
    client.post("/items/command-then-query", json={"name": "First"})

    response = client.get("/items")
    assert len(response.json()) == 2  # noqa: PLR2004
