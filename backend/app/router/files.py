"""
Files API router backed by MinIO (S3-compatible)
"""

from typing import Optional
from datetime import timedelta
from uuid import uuid4
from fastapi import APIRouter, UploadFile, File, HTTPException, Depends, Query
from fastapi.responses import JSONResponse, RedirectResponse
from sqlalchemy.orm import Session
from minio import Minio

from app.crud.files import file as file_db
from app.config import settings
from app.models import BaseResponse
from app.schemas.files import FileUploadResponse, FilePresignResponse, FileCreate
from app.database import get_db
from app.minio import get_minio_client


router = APIRouter(
    prefix="/files",
    tags=["files"],
    responses={
        404: {"description": "Not found"},
        422: {"description": "Validation error"}
    }
)


@router.post("/upload", response_model=FileUploadResponse, summary="Upload a file")
async def upload_file(
    file: UploadFile = File(...),
    folder: Optional[str] = Query(None, description="Optional folder/prefix"),
    client: Minio = Depends(get_minio_client),
    db: Session = Depends(get_db)
) -> FileUploadResponse:
    """
    Upload a file to the default MinIO bucket.
    """
    suffix = file.filename.split(".")[-1] if "." in file.filename else "bin"
    object_name = f"{folder.strip('/') + '/' if folder else ''}{uuid4().hex}.{suffix}"
    
    
    # Upload the file stream
    client.put_object(
        bucket_name=settings.minio_bucket,
        object_name=object_name,
        data=file.file,
        length=-1,
        part_size=5 * 1024 * 1024,
        content_type=file.content_type or "application/octet-stream",
    )
    
    # Create file record
    obj_in = FileCreate(
        object_key=object_name,
        mime_type=file.content_type or "application/octet-stream",
        size_bytes=file.size
    )
    
    file_obj = file_db.create(db=db, obj_in=obj_in)
    
    return FileUploadResponse(
        id=file_obj.id,
        object_key=file_obj.object_key,
        mime_type=file_obj.mime_type,
        size_bytes=file_obj.size_bytes,
    )


@router.delete("/", response_model=BaseResponse, summary="Delete a file")
async def delete_file(
    key: str = Query(..., description="Object key to delete"),
    client: Minio = Depends(get_minio_client),
    db: Session = Depends(get_db)
) -> BaseResponse:
    """
    Delete an object from the default bucket.
    """
    # Delete file from MinIO
    client.remove_object(
        bucket_name=settings.minio_bucket,
        object_name=key,
    )
    
    # Delete file record
    file_obj = file_db.delete(db=db, file_id=key)
    if not file_obj:
        raise HTTPException(status_code=404, detail="File not found")
    
    return BaseResponse(message=f"File {file_obj.id} with object key {key} deleted successfully")


@router.get("/presign", response_model=FilePresignResponse, summary="Get a presigned download URL")
async def presign_download(
    key: str = Query(..., description="Object key to download"),
    expires: int = Query(3600, ge=1, le=7 * 24 * 3600, description="Expiry seconds"),
    client: Minio = Depends(get_minio_client)
):
    """
    Generate a presigned URL for downloading an object.
    """
    try:
        url = client.presigned_get_object(
            bucket_name=settings.minio_bucket,
            object_name=key,
            expires=timedelta(seconds=expires),
        )
        return FilePresignResponse(url=url)
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Presign failed: {exc}")


@router.get("/presign-redirect", summary="Redirect to a presigned URL")
async def presign_redirect(
    key: str = Query(..., description="Object key to download"),
    expires: int = Query(3600, ge=1, le=7 * 24 * 3600, description="Expiry seconds"),
    client: Minio = Depends(get_minio_client)
):
    """
    Generate a presigned URL and redirect to it. Useful for <img src=...> and direct downloads.
    """
    try:
        url = client.presigned_get_object(
            bucket_name=settings.minio_bucket,
            object_name=key,
            expires=timedelta(seconds=expires),
        )
        return RedirectResponse(url=url, status_code=307)
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Presign redirect failed: {exc}")