"""
Application configuration using Pydantic Settings
"""

import os
from typing import List
from pydantic import Field, field_validator
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """
    Application settings
    """
    
    # App Basic Settings
    app_name: str = "[Project name] Backend"
    debug: bool = Field(default=True, description="Debug mode")
    version: str = "0.1.0"
    description: str = "[Project name] Backend API"
    
    # Server Settings
    host: str = Field(default="127.0.0.1", description="Server host")
    port: int = Field(default=8000, description="Server port")
    
    # CORS Settings
    allowed_hosts: List[str] = Field(
        default=["*"], 
        description="Allowed hosts for CORS"
    )
    allowed_origins: List[str] = Field(
        default=["http://localhost:3000", "http://127.0.0.1:3000"],
        description="Allowed origins for CORS"
    )
    
    # Database Settings
    database_url: str = Field(
        default="postgresql://backend_user:backend_password@localhost:5432/backend_db", 
        description="Database connection URL"
    )
    database_echo: bool = Field(
        default=False,
        description="Enable SQLAlchemy query logging"
    )
    
    # Security Settings
    secret_key: str = Field(
        default="your-secret-key-change-this-in-production",
        description="Secret key for JWT and other cryptographic operations"
    )
    
    # JWT Settings
    jwt_algorithm: str = Field(
        default="HS256",
        description="JWT algorithm for token encoding/decoding"
    )
    access_token_expire_minutes: int = Field(
        default=30,
        description="Access token expiration time in minutes"
    )
    refresh_token_expire_days: int = Field(
        default=30,
        description="Refresh token expiration time in days"
    )
    
    # API Settings
    api_prefix: str = Field(default="/api/v1", description="API prefix")
    
    # Object Storage (MinIO/S3-compatible)
    minio_endpoint: str = Field(default="localhost:9000", description="MinIO endpoint host:port")
    minio_access_key: str = Field(default="minioadmin", description="MinIO access key")
    minio_secret_key: str = Field(default="minioadmin", description="MinIO secret key")
    minio_region: str = Field(default="us-east-1", description="MinIO region")
    minio_secure: bool = Field(default=False, description="Use HTTPS to access MinIO")
    minio_bucket: str = Field(default="files", description="Default bucket for file storage")
    
    @field_validator("secret_key")
    @classmethod
    def validate_secret_key(cls, v):
        if len(v) < 16:
            raise ValueError("Secret key must be at least 16 characters long")
        return v
    
    class Config:
        env_file = ".env"
        case_sensitive = False


# Create settings instance
settings = Settings()
