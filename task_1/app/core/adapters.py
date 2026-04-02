from functools import lru_cache

from app.core.config import settings
from app.storage.base import StorageAdapter
from app.storage.s3 import S3StorageAdapter


@lru_cache
def get_storage_adapter() -> StorageAdapter:
    return S3StorageAdapter(
        bucket=settings.MINIO_BUCKET,
        endpoint=settings.MINIO_ENDPOINT,
        public_endpoint=settings.MINIO_PUBLIC_ENDPOINT,
        access_key=settings.MINIO_ACCESS_KEY,
        secret_key=settings.MINIO_SECRET_KEY,
        region=settings.MINIO_REGION,
        presigned_ttl_seconds=settings.MINIO_PRESIGNED_TTL_SECONDS,
    )
