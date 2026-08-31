from fastapi import APIRouter, File, UploadFile
import httpx

router = APIRouter(
    prefix="/api/v1/files",
    tags=["Files"],
)

FILE_SERVICE_URL = "http://file-service:8000"


@router.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    files = {
        "file": (
            file.filename,
            await file.read(),
            file.content_type,
        )
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{FILE_SERVICE_URL}/api/v1/files/upload",
            files=files,
            timeout=120.0,
        )

    response.raise_for_status()
    return response.json()


@router.get("")
async def list_files():
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{FILE_SERVICE_URL}/api/v1/files",
            timeout=30.0,
        )

    response.raise_for_status()
    return response.json()


@router.get("/{file_id}/transcription")
async def get_transcription(file_id: int):
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{FILE_SERVICE_URL}/api/v1/files/{file_id}/transcription",
            timeout=30.0,
        )

    response.raise_for_status()
    return response.json()
