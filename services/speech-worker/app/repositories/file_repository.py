from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.audio_file import AudioFile


class FileRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_by_id(self, file_id: int) -> AudioFile | None:
        result = await self.db.execute(
            select(AudioFile).where(AudioFile.id == file_id)
        )
        return result.scalar_one_or_none()

    async def update_status(
        self,
        file_id: int,
        status: str,
    ) -> AudioFile | None:
        file = await self.get_by_id(file_id)

        if file is None:
            return None

        file.status = status

        await self.db.commit()
        await self.db.refresh(file)

        return file
