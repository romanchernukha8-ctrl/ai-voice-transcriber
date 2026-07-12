from app.models.audio_file import AudioFile
from app.repositories.file_repository import FileRepository
from app.storage.service import StorageService
from fastapi import UploadFile


class FileService:
    def __init__(
        self,
        repository: FileRepository,
        storage: StorageService,
    ):
        self.repository = repository
        self.storage = storage

    async def upload(
            self,
            file: UploadFile,
            owner_id: int,
    ) -> AudioFile:
        object_name, original_name = self.storage.upload_file(file)

        audio_file = AudioFile(
            owner_id=owner_id,
            filename=original_name,
            object_name=object_name,
            content_type=file.content_type,
            status="uploaded",
        )

        return await self.repository.create(audio_file)