from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.transcription import Transcription


class TranscriptionRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(
        self,
        transcription: Transcription,
    ) -> Transcription:
        self.db.add(transcription)

        await self.db.commit()
        await self.db.refresh(transcription)

        return transcription

    async def get_by_file_id(
        self,
        file_id: int,
    ) -> Transcription | None:
        result = await self.db.execute(
            select(Transcription).where(
                Transcription.file_id == file_id
            )
        )

        return result.scalar_one_or_none()
