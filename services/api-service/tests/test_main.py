import os

os.environ["DATABASE_HOST"] = "localhost"
os.environ["DATABASE_PORT"] = "5432"
os.environ["DATABASE_NAME"] = "test"
os.environ["DATABASE_USER"] = "test"
os.environ["DATABASE_PASSWORD"] = "test"

from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_root():
    response = client.get("/")

    assert response.status_code == 200

    data = response.json()

    assert data["service"] == "AI Voice Transcriber API"
    assert data["version"] == "0.1.0"
    assert data["status"] == "running"


def test_health():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}
