from uuid import uuid4

from minio.error import S3Error
from fastapi import UploadFile

from app.core.config import settings
from app.storage.minio_client import get_client


class StorageService:
    def __init__(self):
        self.client = get_client()

    def upload_file(self, file: UploadFile) -> tuple[str, str]:
        object_name = f"{uuid4()}-{file.filename}"

        self.client.put_object(
            bucket_name=settings.minio_bucket,
            object_name=object_name,
            data=file.file,
            length=-1,
            part_size=10 * 1024 * 1024,
            content_type=file.content_type,
        )

        return object_name, file.filename