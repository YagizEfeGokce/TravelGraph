import pytest
from fastapi.testclient import TestClient


def test_list_destinations(client: TestClient):
    response = client.get("/api/destinations")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)


def test_get_destination(client: TestClient):
    # list destinations first to obtain a valid id
    list_resp = client.get("/api/destinations")
    assert list_resp.status_code == 200
    destinations = list_resp.json()

    if not destinations:
        pytest.skip("No seeded destinations available")

    dest_id = destinations[0]["id"]
    response = client.get(f"/api/destinations/{dest_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == dest_id


def test_get_destination_not_found(client: TestClient):
    response = client.get("/api/destinations/nonexistent-id")
    assert response.status_code == 404
