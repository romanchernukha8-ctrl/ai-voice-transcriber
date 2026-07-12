from minio import Minio

from app.core.config import settings


client = Minio(
    endpoint=settings.minio_endpoint,
    access_key=settings.minio_access_key,
    secret_key=settings.minio_secret_key,
    secure=settings.minio_secure,
)


def get_client() -> Minio:
    return client


def create_bucket_if_not_exists() -> None:
    if not client.bucket_exists(settings.minio_bucket):
        client.make_bucket(settings.minio_bucket)
        print(f"Bucket '{settings.minio_bucket}' created.")