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
    client: Minio = Depends(get_minio_client),
    db: Session = Depends(get_db)
) -> FileUploadResponse:
    """
    Upload a file to the default MinIO bucket using file ID as object key.
    """
    # Create file record first to get the UUID
    obj_in = FileCreate(
        mime_type=file.content_type or "application/octet-stream",
        size_bytes=file.size if file.size is not None else 0
    )
    file_obj = file_db.create(db=db, obj_in=obj_in)
    
    # Use the file ID as the object key in MinIO
    object_key = str(file_obj.id)
    
    # Upload the file stream using file ID as object key
    client.put_object(
        bucket_name=settings.minio_bucket,
        object_name=object_key,
        data=file.file,
        length=-1,
        part_size=5 * 1024 * 1024,
        content_type=file.content_type or "application/octet-stream",
    )
    
    return FileUploadResponse.model_validate(file_obj)


@router.delete("/", response_model=BaseResponse, summary="Delete a file")
async def delete_file(
    id: str = Query(..., description="File ID to delete"),
    client: Minio = Depends(get_minio_client),
    db: Session = Depends(get_db)
) -> BaseResponse:
    """
    Delete a file from MinIO and database using file ID.
    """
    # Delete file record first (to validate it exists)
    file_obj = file_db.delete(db=db, file_id=id)
    if not file_obj:
        raise HTTPException(status_code=404, detail="File not found")
    
    # Delete file from MinIO using file ID as object key
    client.remove_object(
        bucket_name=settings.minio_bucket,
        object_name=id,
    )
    
    return BaseResponse(message=f"File {id} deleted successfully")


@router.get("/presign", response_model=FilePresignResponse, summary="Get a presigned download URL")
async def presign_download(
    id: str = Query(..., description="File ID to download"),
    expires: int = Query(3600, ge=1, le=7 * 24 * 3600, description="Expiry seconds"),
    client: Minio = Depends(get_minio_client),
    db: Session = Depends(get_db)
):
    """
    Generate a presigned URL for downloading a file using file ID.
    """
    # Verify file exists in database
    file_obj = file_db.get(db=db, file_id=id)
    if not file_obj:
        raise HTTPException(status_code=404, detail="File not found")
    
    try:
        url = client.presigned_get_object(
            bucket_name=settings.minio_bucket,
            object_name=id,
            expires=timedelta(seconds=expires),
        )
        return FilePresignResponse(url=url)
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Presign failed: {exc}")


@router.get("/presign-redirect", summary="Redirect to a presigned URL")
async def presign_redirect(
    id: str = Query(..., description="File ID to download"),
    expires: int = Query(3600, ge=1, le=7 * 24 * 3600, description="Expiry seconds"),
    client: Minio = Depends(get_minio_client),
    db: Session = Depends(get_db)
):
    """
    Generate a presigned URL and redirect to it using file ID. Useful for <img src=...> and direct downloads.
    """
    # Verify file exists in database
    file_obj = file_db.get(db=db, file_id=id)
    if not file_obj:
        raise HTTPException(status_code=404, detail="File not found")
    
    try:
        url = client.presigned_get_object(
            bucket_name=settings.minio_bucket,
            object_name=id,
            expires=timedelta(seconds=expires),
        )
        return RedirectResponse(url=url, status_code=307)
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Presign redirect failed: {exc}")