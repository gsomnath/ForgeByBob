from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from datetime import datetime
from enum import Enum


class PublicationSite(str, Enum):
    MEDIUM = "medium"
    WORDPRESS = "wordpress"
    GHOST = "ghost"
    CUSTOM = "custom"


class BlogStatus(str, Enum):
    DRAFT = "draft"
    IN_PROGRESS = "in_progress"
    REVIEW = "review"
    COMPLETED = "completed"
    PUBLISHED = "published"


class BlogBase(BaseModel):
    title: str
    description: Optional[str] = None
    tags: List[str] = []
    publication_site: Optional[PublicationSite] = None


class BlogCreate(BlogBase):
    initial_prompt: str


class BlogUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    tags: Optional[List[str]] = None
    publication_site: Optional[PublicationSite] = None
    status: Optional[BlogStatus] = None


class Blog(BlogBase):
    id: str
    status: BlogStatus
    created_at: datetime
    updated_at: datetime
    folder_path: str
    current_version: int
    latest_content: Optional[str] = None  # Store the latest generated content
    
    class Config:
        from_attributes = True


class BlogVersion(BaseModel):
    id: str
    blog_id: str
    version_number: int
    content: str
    prompt_used: str
    created_at: datetime
    created_by: str = "system"
    
    class Config:
        from_attributes = True


class CommentCreate(BaseModel):
    content: str
    requested_changes: Optional[str] = None


class Comment(BaseModel):
    id: str
    blog_id: str
    content: str
    requested_changes: Optional[str] = None
    created_at: datetime
    
    class Config:
        from_attributes = True


class SettingsBase(BaseModel):
    gemini_api_key: Optional[str] = None
    source_folder: Optional[str] = None
    default_publication_site: Optional[PublicationSite] = None
    
    # Google Cloud Imagen Configuration
    google_cloud_project: Optional[str] = None
    google_cloud_location: Optional[str] = "us-central1"
    google_cloud_credentials_path: Optional[str] = None
    imagen_enabled: bool = False
    imagen_model: str = "imagen-4.0-generate-001"  # Updated to latest model


class SettingsCreate(SettingsBase):
    pass


class SettingsUpdate(SettingsBase):
    pass


class Settings(SettingsBase):
    id: str
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class GeminiAPILog(BaseModel):
    id: str
    request_timestamp: datetime
    blog_id: Optional[str] = None
    prompt: str
    model_used: str
    response_content: Optional[str] = None
    response_timestamp: Optional[datetime] = None
    success: bool
    error_message: Optional[str] = None
    processing_time_ms: Optional[int] = None
    
    class Config:
        from_attributes = True


class ImagenAPILog(BaseModel):
    id: str
    request_timestamp: datetime
    blog_id: Optional[str] = None
    prompt: str
    model_used: str = "imagen-3"
    image_urls: Optional[List[str]] = None
    response_timestamp: Optional[datetime] = None
    success: bool
    error_message: Optional[str] = None
    processing_time_ms: Optional[int] = None
    
    class Config:
        from_attributes = True


class APIResponse(BaseModel):
    success: bool
    message: str
    data: Optional[Any] = None


class ErrorResponse(BaseModel):
    success: bool = False
    message: str
    error_code: Optional[str] = None
    details: Optional[Dict[str, Any]] = None
