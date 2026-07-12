from app.storage.minio_client import get_client
from app.core.config import settings

client = get_client()

print(client)

print(client.bucket_exists(settings.minio_bucket))