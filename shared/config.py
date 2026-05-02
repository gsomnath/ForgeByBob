from pydantic_settings import BaseSettings
from typing import Optional
import secrets


class AppSettings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    # IBM Cloud Authentication
    ibm_cloud_api_key: Optional[str] = None
    
    # IBM watsonx.ai Configuration
    watsonx_project_id: Optional[str] = None
    watsonx_url: str = "https://us-south.ml.cloud.ibm.com"
    watsonx_model_id: str = "ibm/granite-4-h-small"
    
    # IBM Cloud Object Storage
    cos_instance_id: Optional[str] = None
    cos_api_key: Optional[str] = None
    cos_endpoint: Optional[str] = None
    cos_bucket: Optional[str] = None
    
    # IBM watsonx Orchestrate
    orchestrate_instance_id: Optional[str] = None
    orchestrate_api_key: Optional[str] = None
    orchestrate_url: Optional[str] = None
    orchestrate_workspace_id: Optional[str] = None
    
    # IBM Watson NLU
    nlu_instance_id: Optional[str] = None
    nlu_api_key: Optional[str] = None
    nlu_url: Optional[str] = None
    
    # IBM Cloudant
    cloudant_instance_id: Optional[str] = None
    cloudant_api_key: Optional[str] = None
    cloudant_url: Optional[str] = None
    cloudant_account: Optional[str] = None
    cloudant_database: Optional[str] = None
    
    # IBM watsonx Governance
    gov_instance_id: Optional[str] = None
    gov_api_key: Optional[str] = None
    gov_url: Optional[str] = None
    
    # WatsonX is the primary AI service
    use_watsonx: bool = True
    
    # File System Configuration
    source_folder: str = "./blogs"
    
    # Database Configuration
    database_url: str = "sqlite:///./app.db"
    
    # Security - MUST be set via environment variable in production
    secret_key: Optional[str] = None
    access_token_expire_minutes: int = 30
    
    # Agent Configuration
    max_iterations: int = 3
    quality_threshold: float = 7.0
    
    # Service Ports
    api_gateway_port: int = 8000
    blog_service_port: int = 8001
    settings_service_port: int = 8002
    ui_service_port: int = 8003
    orchestration_service_port: int = 8004
    
    # Service URLs
    blog_service_url: str = "http://localhost:8001"
    settings_service_url: str = "http://localhost:8002"
    orchestration_service_url: str = "http://localhost:8004"
    
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
