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

    assert data["service"] == "file-service"
    assert data["status"] == "running"


def test_health():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}


def test_get_transcription_not_found(monkeypatch):
    from app.api.v1.files import get_transcription

    async def mock_get_by_file_id(self, file_id):
        return None

    monkeypatch.setattr(
        "app.services.transcription_service.TranscriptionService.get_by_file_id",
        mock_get_by_file_id,
    )

    response = client.get("/api/v1/files/999/transcription")

    assert response.status_code == 404
    assert response.json() == {"detail": "Transcription not found"}