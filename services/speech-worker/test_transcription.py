import uuid

import pytest

from app.db.base import Base
from app.db.session import async_session_factory, engine
from app.models.audio_file import AudioFile
from app.models.transcription import Transcription
from app.repositories.transcription_repository import TranscriptionRepository


@pytest.mark.asyncio
async def test_create_transcription():
    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.create_all)

    async with async_session_factory() as session:
        object_name = f"test-transcription-{uuid.uuid4()}.mp3"

        audio_file = AudioFile(
            owner_id=1,
            filename="test-audio.mp3",
            object_name=object_name,
            content_type="audio/mpeg",
            status="uploaded",
        )

        session.add(audio_file)
        await session.commit()
        await session.refresh(audio_file)

        repository = TranscriptionRepository(session)

        transcription = await repository.create(
            file_id=audio_file.id,
            text="This is a test transcription.",
            language="en",
        )

        assert transcription.id is not None
        assert transcription.file_id == audio_file.id
        assert transcription.text == "This is a test transcription."
        assert transcription.language == "en"

        await session.delete(transcription)
        await session.flush()

        await session.delete(audio_file)
        await session.commit()