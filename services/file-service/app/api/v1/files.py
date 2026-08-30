from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.dependencies import get_db
from app.repositories.file_repository import FileRepository
from app.repositories.transcription_repository import TranscriptionRepository
from app.schemas.file import FileResponse
from app.schemas.transcription import TranscriptionResponse
from app.services.file_service import FileService
from app.services.transcription_service import TranscriptionService
from app.storage.service import StorageService
from app.messaging.publisher import RabbitPublisher


router = APIRouter(
    prefix="/api/v1/files",
    tags=["Files"],
)


@router.post(
    "/upload",
    response_model=FileResponse,
    summary="Upload audio file",
)
async def upload_file(
    file: UploadFile = File(...),
    db: AsyncSession = Depends(get_db),
):
    repository = FileRepository(db)
    storage = StorageService()
    publisher = RabbitPublisher()

    service = FileService(
        repository=repository,
        storage=storage,
        publisher=publisher,
    )

    # Временно используем owner_id = 1
    # После подключения JWT заменим на current_user.id
    return await service.upload(
        file=file,
        owner_id=1,
    )


@router.get(
    "",
    response_model=list[FileResponse],
    summary="List uploaded files",
)
async def list_files(
    db: AsyncSession = Depends(get_db),
):
    repository = FileRepository(db)

    storage = StorageService()

    service = FileService(
        repository=repository,
        storage=storage,
    )

    # Временно используем owner_id = 1
    # После подключения JWT заменим на current_user.id
    return await service.list(owner_id=1)

@router.get(
    "/{file_id}/transcription",
    response_model=TranscriptionResponse,
    summary="Get file transcription",
)
async def get_transcription(
    file_id: int,
    db: AsyncSession = Depends(get_db),
):
    repository = TranscriptionRepository(db)

    service = TranscriptionService(
        repository=repository,
    )

    transcription = await service.get_by_file_id(file_id)

    if transcription is None:
        raise HTTPException(
            status_code=404,
            detail="Transcription not found",
        )

    return transcription