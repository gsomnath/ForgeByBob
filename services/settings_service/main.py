from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from typing import Optional
import os
from pathlib import Path
import sys
import json
import logging
from datetime import datetime, timezone

# Add the project root to the Python path
project_root = Path(__file__).parent.parent.parent
sys.path.append(str(project_root))

from shared.config import settings as app_settings
from shared.models import Settings, SettingsCreate, SettingsUpdate, APIResponse
from shared.utils import generate_id, ensure_directory_exists

# Persistent storage
DATA_DIR = Path("data")
SETTINGS_DB_FILE = DATA_DIR / "settings.json"

# In-memory storage for settings (loaded from persistent storage)
settings_db = {}
SETTINGS_ID = "main_settings"

def ensure_data_directory():
    """Ensure data directory exists."""
    DATA_DIR.mkdir(exist_ok=True)

def load_settings_from_file():
    """Load settings from persistent storage."""
    global settings_db
    try:
        if SETTINGS_DB_FILE.exists():
            with open(SETTINGS_DB_FILE, 'r', encoding='utf-8') as f:
                data = json.load(f)
                # Convert back to Settings objects
                for settings_id, settings_data in data.items():
                    # Convert datetime strings back to datetime objects
                    if 'created_at' in settings_data:
                        settings_data['created_at'] = datetime.fromisoformat(settings_data['created_at'].replace('Z', '+00:00'))
                    if 'updated_at' in settings_data:
                        settings_data['updated_at'] = datetime.fromisoformat(settings_data['updated_at'].replace('Z', '+00:00'))
                    
                    # Ensure all IBM watsonx fields have proper defaults if missing
                    if 'ibm_cloud_api_key' not in settings_data:
                        settings_data['ibm_cloud_api_key'] = None
                    if 'watsonx_project_id' not in settings_data:
                        settings_data['watsonx_project_id'] = None
                    if 'watsonx_url' not in settings_data:
                        settings_data['watsonx_url'] = "https://us-south.ml.cloud.ibm.com"
                    if 'watsonx_model_id' not in settings_data:
                        settings_data['watsonx_model_id'] = "meta-llama/llama-3-3-70b-instruct"
                    
                    settings_db[settings_id] = Settings(**settings_data)
                print(f"Loaded settings from persistent storage")
    except Exception as e:
        print(f"Error loading settings from file: {e}")
        settings_db = {}

def save_settings_to_file():
    """Save settings to persistent storage."""
    try:
        ensure_data_directory()
        # Convert Settings objects to serializable dict
        data = {}
        for settings_id, settings in settings_db.items():
            data[settings_id] = settings.model_dump(mode='json')
        
        with open(SETTINGS_DB_FILE, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
    except Exception as e:
        print(f"Error saving settings to file: {e}")

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Manage application lifecycle."""
    ensure_data_directory()
    load_settings_from_file()
    if SETTINGS_ID not in settings_db:
        default_settings = Settings(
            id=SETTINGS_ID,
            ibm_cloud_api_key=app_settings.ibm_cloud_api_key,
            watsonx_project_id=app_settings.watsonx_project_id,
            watsonx_url=app_settings.watsonx_url,
            watsonx_model_id=app_settings.watsonx_model_id,
            source_folder=app_settings.source_folder,
            default_publication_site=None,
            created_at=datetime.now(timezone.utc),
            updated_at=datetime.now(timezone.utc)
        )
        settings_db[SETTINGS_ID] = default_settings
        save_settings_to_file()
    yield


app = FastAPI(
    title="Settings Service",
    description="Microservice for configuration and settings management",
    version="1.0.0",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    """Root endpoint."""
    return APIResponse(
        success=True,
        message="Settings Service is running",
        data={"version": "1.0.0"}
    )

@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "service": "settings-service"}

@app.get("/settings", response_model=APIResponse)
async def get_settings():
    """Get current application settings."""
    try:
        settings = settings_db.get(SETTINGS_ID)
        if not settings:
            raise HTTPException(status_code=404, detail="Settings not found")
        
        # Return settings without sensitive data for public access
        settings_data = settings.model_dump(mode='json')
        # Mask API key for security
        if settings_data.get("ibm_cloud_api_key"):
            settings_data["ibm_cloud_api_key"] = "***masked***"
        
        return APIResponse(
            success=True,
            message="Settings retrieved successfully",
            data=settings_data
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.put("/settings", response_model=APIResponse)
async def update_settings(settings_update: SettingsUpdate):
    """Update application settings."""
    try:
        current_settings = settings_db.get(SETTINGS_ID)
        if not current_settings:
            # Create new settings if they don't exist
            current_settings = Settings(
                id=SETTINGS_ID,
                created_at=datetime.now(timezone.utc),
                updated_at=datetime.now(timezone.utc)
            )
        
        # Update fields
        if settings_update.ibm_cloud_api_key is not None:
            current_settings.ibm_cloud_api_key = settings_update.ibm_cloud_api_key
        if settings_update.watsonx_project_id is not None:
            current_settings.watsonx_project_id = settings_update.watsonx_project_id
        if settings_update.watsonx_url is not None:
            current_settings.watsonx_url = settings_update.watsonx_url
        if settings_update.watsonx_model_id is not None:
            current_settings.watsonx_model_id = settings_update.watsonx_model_id
        if settings_update.source_folder is not None:
            current_settings.source_folder = settings_update.source_folder
            # Ensure the source folder exists
            ensure_directory_exists(settings_update.source_folder)
        if settings_update.default_publication_site is not None:
            current_settings.default_publication_site = settings_update.default_publication_site
        
        current_settings.updated_at = datetime.now(timezone.utc)
        settings_db[SETTINGS_ID] = current_settings
        save_settings_to_file()  # Save to persistent storage
        
        # Return settings without sensitive data
        settings_data = current_settings.model_dump(mode='json')
        if settings_data.get("ibm_cloud_api_key"):
            settings_data["ibm_cloud_api_key"] = "***masked***"
        
        return APIResponse(
            success=True,
            message="Settings updated successfully",
            data=settings_data
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/settings/validation", response_model=APIResponse)
async def validate_settings():
    """Validate current settings configuration."""
    try:
        settings = settings_db.get(SETTINGS_ID)
        if not settings:
            return APIResponse(
                success=False,
                message="No settings found"
            )
        
        validation_results = {
            "ibm_cloud_api_key": bool(settings.ibm_cloud_api_key),
            "watsonx_project_id": bool(settings.watsonx_project_id),
            "source_folder": bool(settings.source_folder),
            "source_folder_exists": False
        }
        
        # Check if source folder exists
        if settings.source_folder:
            validation_results["source_folder_exists"] = Path(settings.source_folder).exists()
        
        is_valid = all([
            validation_results["ibm_cloud_api_key"],
            validation_results["watsonx_project_id"],
            validation_results["source_folder"],
            validation_results["source_folder_exists"]
        ])
        
        return APIResponse(
            success=True,
            message="Settings validation completed",
            data={
                "is_valid": is_valid,
                "validation_results": validation_results
            }
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/settings/test-watsonx", response_model=APIResponse)
async def test_watsonx_connection():
    """Test IBM watsonx.ai connection with current credentials."""
    try:
        settings = settings_db.get(SETTINGS_ID)
        if not settings or not settings.ibm_cloud_api_key or not settings.watsonx_project_id:
            raise HTTPException(status_code=400, detail="IBM watsonx credentials not configured")
        
        try:
            from ibm_watsonx_ai.foundation_models import ModelInference
            from ibm_watsonx_ai.metanames import GenTextParamsMetaNames as GenParams
            
            logger = logging.getLogger(__name__)
            logger.info(f"Testing watsonx connection with model: {settings.watsonx_model_id}")
            logger.info(f"Project ID: {settings.watsonx_project_id}")
            logger.info(f"URL: {settings.watsonx_url}")
            
            # Configure watsonx credentials
            credentials = {
                "url": settings.watsonx_url,
                "apikey": settings.ibm_cloud_api_key
            }
            
            # Set up model parameters
            parameters = {
                GenParams.MAX_NEW_TOKENS: 100,
                GenParams.TEMPERATURE: 0.7,
                GenParams.TOP_P: 0.9,
                GenParams.TOP_K: 50,
            }
            
            # Initialize the model using ModelInference
            model = ModelInference(
                model_id=settings.watsonx_model_id,
                params=parameters,
                credentials=credentials,
                project_id=settings.watsonx_project_id
            )
            
            logger.info("Model initialized, attempting to generate text...")
            
            # Test with a simple prompt
            response = model.generate_text(prompt="Say 'Hello from IBM watsonx.ai!'")
            
            logger.info(f"Generation successful. Response: {response[:100]}...")
            
            return APIResponse(
                success=True,
                message="watsonx.ai connection successful",
                data={
                    "test_response": str(response),
                    "model": settings.watsonx_model_id,
                    "project_id": settings.watsonx_project_id
                }
            )
            
        except Exception as watsonx_error:
            error_message = str(watsonx_error)
            error_type = type(watsonx_error).__name__
            
            # Log detailed error information
            import traceback
            logger = logging.getLogger(__name__)
            logger.error(f"watsonx.ai connection test failed: {error_type}: {error_message}")
            logger.error(f"Full traceback:\n{traceback.format_exc()}")
            
            # Provide more specific error messages
            if "401" in error_message or "Unauthorized" in error_message:
                error_detail = "Invalid API key. Please check your IBM_CLOUD_API_KEY."
            elif "403" in error_message or "Forbidden" in error_message:
                error_detail = "Access denied. Check if your API key has access to the project."
            elif "404" in error_message or "Not Found" in error_message:
                error_detail = "Project or model not found. Verify WATSONX_PROJECT_ID and model ID."
            elif "429" in error_message or "Too Many Requests" in error_message:
                error_detail = "⏱️ Rate limit exceeded. Your credentials are valid, but you've reached the API limit. Please wait 5-10 minutes before trying again. This is normal with the free tier."
            elif "timeout" in error_message.lower():
                error_detail = "Connection timeout. Check your network connection."
            else:
                error_detail = error_message
            
            return APIResponse(
                success=False,
                message=f"watsonx.ai connection failed: {error_detail}",
                data={
                    "error": error_message,
                    "error_type": error_type,
                    "model": settings.watsonx_model_id,
                    "project_id": settings.watsonx_project_id
                }
            )
    
    except HTTPException:
        raise
    except Exception as e:
        import traceback
        logger = logging.getLogger(__name__)
        logger.error(f"Unexpected error in test_watsonx_connection: {str(e)}")
        logger.error(f"Full traceback:\n{traceback.format_exc()}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/settings/raw", response_model=APIResponse)
async def get_raw_settings():
    """Get raw settings including sensitive data (for internal service use)."""
    try:
        settings = settings_db.get(SETTINGS_ID)
        if not settings:
            raise HTTPException(status_code=404, detail="Settings not found")
        
        return APIResponse(
            success=True,
            message="Raw settings retrieved successfully",
            data=settings.model_dump(mode='json')
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=app_settings.settings_service_port)
