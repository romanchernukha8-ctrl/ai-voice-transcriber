from fastapi import APIRouter, Depends, UploadFile, File
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.dependencies import get_db
from app.repositories.file_repository import FileRepository
from app.schemas.file import FileResponse
from app.services.file_service import FileService
from app.storage.service import StorageService

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

    service = FileService(
        repository=repository,
        storage=storage,
    )

    # Временно используем owner_id = 1
    # После подключения JWT заменим на current_user.id
    return await service.upload(
        file=file,
        owner_id=1,
    )