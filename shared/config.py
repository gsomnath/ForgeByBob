from pydantic_settings import BaseSettings
from typing import Optional
import secrets


class AppSettings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    # Gemini AI Configuration
    gemini_api_key: Optional[str] = None
    
    # File System Configuration
    source_folder: str = "./blogs"
    
    # Database Configuration
    database_url: str = "sqlite:///./app.db"
    
    # Security - MUST be set via environment variable in production
    secret_key: Optional[str] = None
    access_token_expire_minutes: int = 30
    
    # Service Ports
    api_gateway_port: int = 8000
    blog_service_port: int = 8001
    settings_service_port: int = 8002
    ui_service_port: int = 8003
    
    # Service URLs
    blog_service_url: str = "http://localhost:8001"
    settings_service_url: str = "http://localhost:8002"
    
    # Logging
    log_level: str = "INFO"
    
    class Config:
        env_file = ".env"
        case_sensitive = False
        
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Generate a secure random secret key if not provided
        # WARNING: This will change on each restart. Set SECRET_KEY in .env for production
        if not self.secret_key:
            self.secret_key = secrets.token_urlsafe(32)
            print("WARNING: Using auto-generated SECRET_KEY. Set SECRET_KEY in .env for production!")


# Global settings instance
settings = AppSettings()
