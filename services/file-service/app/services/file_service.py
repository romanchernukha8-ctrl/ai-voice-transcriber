from app.models.audio_file import AudioFile
from app.repositories.file_repository import FileRepository
from app.storage.service import StorageService
from fastapi import UploadFile

from app.messaging.publisher import RabbitPublisher


class FileService:
    def __init__(
        self,
        repository: FileRepository,
        storage: StorageService,
        publisher: RabbitPublisher | None = None,
    ):
        self.repository = repository
        self.storage = storage
        self.publisher = publisher

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

        saved_file = await self.repository.create(audio_file)

        self.publisher.publish(
            file_id=saved_file.id,
            object_name=saved_file.object_name,
        )

        self.publisher.close()

        return saved_file

    async def list(self, owner_id: int) -> list[AudioFile]:
        return await self.repository.list(owner_id)

    async def get(self, file_id: int) -> AudioFile | None:
        return await self.repository.get_by_id(file_id)