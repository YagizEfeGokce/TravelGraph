import pytest
from fastapi.testclient import TestClient
from main import app


@pytest.fixture
def client():
    """Returns a TestClient for the FastAPI app.

    Requires FalkorDB to be running on localhost:6379.
    Run with: docker compose up -d
    """
    return TestClient(app)
