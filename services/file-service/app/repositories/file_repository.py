from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.audio_file import AudioFile


class FileRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, file: AudioFile) -> AudioFile:
        self.db.add(file)
        await self.db.commit()
        await self.db.refresh(file)
        return file

    async def get_by_id(self, file_id: int) -> AudioFile | None:
        result = await self.db.execute(
            select(AudioFile).where(AudioFile.id == file_id)
        )
        return result.scalar_one_or_none()

    async def list(self, owner_id: int) -> list[AudioFile]:
        result = await self.db.execute(
            select(AudioFile)
            .where(AudioFile.owner_id == owner_id)
            .order_by(AudioFile.created_at.desc())
        )

        return list(result.scalars().all())

    async def update(self, file: AudioFile) -> AudioFile:
        await self.db.commit()
        await self.db.refresh(file)
        return file

    async def delete(self, file: AudioFile) -> None:
        await self.db.delete(file)
        await self.db.commit()