import asyncio

from botocore.exceptions import BotoCoreError, ClientError
from fastapi import HTTPException

from app.storage.base import StorageAdapter


class S3StorageAdapter(StorageAdapter):
    def __init__(
        self,
        bucket: str,
        endpoint: str,
        public_endpoint: str,
        access_key: str,
        secret_key: str,
        region: str,
        presigned_ttl_seconds: int,
    ):
        try:
            import boto3
        except ImportError as exc:
            raise RuntimeError(
                "boto3 is required for MinIO upload. Install it with: pip install boto3"
            ) from exc

        self.bucket = bucket
        self.endpoint = endpoint.rstrip("/")
        self.public_endpoint = public_endpoint.rstrip("/")
        self.region = region
        self.presigned_ttl_seconds = presigned_ttl_seconds
        self.client = boto3.client(
            "s3",
            endpoint_url=self.endpoint,
            aws_access_key_id=access_key,
            aws_secret_access_key=secret_key,
            region_name=region,
        )
        self.public_client = boto3.client(
            "s3",
            endpoint_url=self.public_endpoint,
            aws_access_key_id=access_key,
            aws_secret_access_key=secret_key,
            region_name=region,
        )

    def _ensure_bucket(self) -> None:
        try:
            self.client.head_bucket(Bucket=self.bucket)
            return
        except ClientError as exc:
            error_code = str(exc.response.get("Error", {}).get("Code", ""))
            if error_code not in {"404", "NoSuchBucket", "NotFound"}:
                raise

        if self.region == "us-east-1":
            self.client.create_bucket(Bucket=self.bucket)
            return

        self.client.create_bucket(
            Bucket=self.bucket,
            CreateBucketConfiguration={"LocationConstraint": self.region},
        )

    async def upload(self, content: bytes, key: str, content_type: str) -> str:
        try:
            await asyncio.to_thread(self._ensure_bucket)
            await asyncio.to_thread(
                self.client.put_object,
                Bucket=self.bucket,
                Key=key,
                Body=content,
                ContentType=content_type,
            )
        except (ClientError, BotoCoreError) as exc:
            raise HTTPException(status_code=502, detail=f"MinIO upload failed: {exc}") from exc

        return await asyncio.to_thread(
            self.public_client.generate_presigned_url,
            "get_object",
            {"Bucket": self.bucket, "Key": key},
            self.presigned_ttl_seconds,
            "GET",
        )

    async def check(self) -> None:
        try:
            await asyncio.to_thread(self._ensure_bucket)
            await asyncio.to_thread(self.client.head_bucket, Bucket=self.bucket)
        except (ClientError, BotoCoreError) as exc:
            raise HTTPException(status_code=502, detail=f"MinIO check failed: {exc}") from exc
