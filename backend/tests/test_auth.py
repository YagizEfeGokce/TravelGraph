from fastapi.testclient import TestClient


def test_register_success(client: TestClient):
    response = client.post(
        "/api/auth/register",
        json={
            "email": "test_register_1@example.com",
            "name": "Test User",
            "password": "SecurePass1",
        },
    )
    assert response.status_code == 201
    data = response.json()
    assert "access_token" in data
    assert "refresh_token" in data
    assert "user" in data


def test_register_duplicate_email(client: TestClient):
    payload = {
        "email": "test_register_2@example.com",
        "name": "Test User",
        "password": "SecurePass1",
    }
    response = client.post("/api/auth/register", json=payload)
    assert response.status_code == 201

    response2 = client.post("/api/auth/register", json=payload)
    assert response2.status_code == 409


def test_login_success(client: TestClient):
    # register first
    email = "test_login_1@example.com"
    password = "SecurePass1"
    client.post(
        "/api/auth/register",
        json={"email": email, "name": "Login User", "password": password},
    )

    response = client.post(
        "/api/auth/login",
        data={"username": email, "password": password},
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert "refresh_token" in data
    assert "user" in data


def test_login_wrong_password(client: TestClient):
    email = "test_login_2@example.com"
    password = "SecurePass1"
    client.post(
        "/api/auth/register",
        json={"email": email, "name": "Login User", "password": password},
    )

    response = client.post(
        "/api/auth/login",
        data={"username": email, "password": "WrongPass1"},
    )
    assert response.status_code == 401


def test_me_with_token(client: TestClient):
    email = "test_me_1@example.com"
    password = "SecurePass1"
    register_resp = client.post(
        "/api/auth/register",
        json={"email": email, "name": "Me User", "password": password},
    )
    assert register_resp.status_code == 201
    token = register_resp.json()["access_token"]

    response = client.get(
        "/api/auth/me",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == email


def test_me_without_token(client: TestClient):
    response = client.get("/api/auth/me")
    assert response.status_code == 401
