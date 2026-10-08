from io import BytesIO

import pytest
from fastapi import UploadFile

from app.services.file_service import FileService


class FakeStorage:
    def __init__(self):
        self.uploaded_file = None

    def upload_file(self, file):
        self.uploaded_file = file
        return "uploads/test-audio.mp3", "test-audio.mp3"


class FakeRepository:
    def __init__(self):
        self.created_file = None

    async def create(self, audio_file):
        audio_file.id = 1
        self.created_file = audio_file
        return audio_file

    async def get_by_id(self, file_id):
        return None


class FakePublisher:
    def __init__(self):
        self.published = None
        self.closed = False

    def publish(self, file_id, object_name):
        self.published = {
            "file_id": file_id,
            "object_name": object_name,
        }

    def close(self):
        self.closed = True


@pytest.mark.anyio
async def test_upload_success():
    storage = FakeStorage()
    repository = FakeRepository()
    publisher = FakePublisher()

    service = FileService(
        repository=repository,
        storage=storage,
        publisher=publisher,
    )

    upload = UploadFile(
        filename="test-audio.mp3",
        file=BytesIO(b"audio-data"),
        headers={"content-type": "audio/mpeg"},
    )

    result = await service.upload(
        file=upload,
        owner_id=1,
    )

    assert result.id == 1
    assert result.owner_id == 1
    assert result.filename == "test-audio.mp3"
    assert result.object_name == "uploads/test-audio.mp3"
    assert result.content_type == "audio/mpeg"
    assert result.status == "uploaded"

    assert storage.uploaded_file is upload
    assert repository.created_file is result

    assert publisher.published == {
        "file_id": 1,
        "object_name": "uploads/test-audio.mp3",
    }

    assert publisher.closed is True


@pytest.mark.anyio
async def test_get_unknown_file():
    repository = FakeRepository()
    storage = FakeStorage()

    service = FileService(
        repository=repository,
        storage=storage,
    )

    result = await service.get(file_id=999)

    assert result is None
