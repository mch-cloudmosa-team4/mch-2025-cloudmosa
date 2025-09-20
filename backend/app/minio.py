"""
Utility functions for the MinIO client
"""

import logging

from typing import Optional

try:
    from minio import Minio
    from minio.error import S3Error
except Exception:  # pragma: no cover - optional dependency until installed
    Minio = None  # type: ignore
    S3Error = Exception  # type: ignore

from app.config import settings


def create_minio_client() -> Optional["Minio"]:
    """
    Create and return a MinIO client using settings.
    Returns None if the minio package is not installed yet.
    """
    if Minio is None:
        return None
    return Minio(
        endpoint=settings.minio_endpoint,
        access_key=settings.minio_access_key,
        secret_key=settings.minio_secret_key,
        secure=settings.minio_secure,
        region=settings.minio_region,
    )


def ensure_bucket_exists(client: "Minio", bucket_name: str) -> None:
    """
    Ensure the given bucket exists; create if missing.
    """
    try:
        if not client.bucket_exists(bucket_name):
            client.make_bucket(bucket_name)
    except S3Error as exc:  # type: ignore
        logging.getLogger("[Project name]-backend").error(f"MinIO bucket error: {exc}")
        raise


def get_minio_client():
    """
    Dependency that yields a MinIO client instance for request scope.
    """
    client = create_minio_client()
    ensure_bucket_exists(client, settings.minio_bucket)
    try:
        yield client
    finally:
        pass