import asyncio

from app.db.session import async_session_factory
from app.repositories.transcription_repository import TranscriptionRepository


async def test_create_transcription():
    async with async_session_factory() as session:
        repository = TranscriptionRepository(session)

        transcription = await repository.create(
            file_id=3,
            text="This is a test transcription.",
            language="en",
        )

        print(f"Transcription created: id={transcription.id}")
        print(f"File ID: {transcription.file_id}")
        print(f"Text: {transcription.text}")
        print(f"Language: {transcription.language}")


if __name__ == "__main__":
    asyncio.run(test_create_transcription())
