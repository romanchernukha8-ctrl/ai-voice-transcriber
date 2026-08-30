from app.models.transcription import Transcription
from app.repositories.transcription_repository import TranscriptionRepository


class TranscriptionService:
    def __init__(
        self,
        repository: TranscriptionRepository,
    ):
        self.repository = repository

    async def get_by_file_id(
        self,
        file_id: int,
    ) -> Transcription | None:
        return await self.repository.get_by_file_id(file_id)
