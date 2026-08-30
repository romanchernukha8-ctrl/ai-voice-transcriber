from app.config import settings
from app.storage.minio_client import get_client


class StorageService:
    def __init__(self):
        self.client = get_client()
        self.bucket = settings.minio_bucket

    def download_file(
        self,
        object_name: str,
        destination: str,
    ) -> str:
        self.client.fget_object(
            bucket_name=self.bucket,
            object_name=object_name,
            file_path=destination,
        )

        return destination