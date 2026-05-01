from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from typing import Optional
import os
from pathlib import Path
import sys
import json
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
                    
                    # Ensure all Google Cloud Imagen fields have proper defaults if missing
                    if 'google_cloud_project' not in settings_data:
                        settings_data['google_cloud_project'] = None
                    if 'google_cloud_location' not in settings_data:
                        settings_data['google_cloud_location'] = "us-central1"
                    if 'google_cloud_credentials_path' not in settings_data:
                        settings_data['google_cloud_credentials_path'] = None
                    if 'imagen_enabled' not in settings_data:
                        settings_data['imagen_enabled'] = False
                    if 'imagen_model' not in settings_data:
                        settings_data['imagen_model'] = "imagen-3"
                    
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
            gemini_api_key=app_settings.gemini_api_key,
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
        if settings_data.get("gemini_api_key"):
            settings_data["gemini_api_key"] = "***masked***"
        
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
        if settings_update.gemini_api_key is not None:
            current_settings.gemini_api_key = settings_update.gemini_api_key
        if settings_update.source_folder is not None:
            current_settings.source_folder = settings_update.source_folder
            # Ensure the source folder exists
            ensure_directory_exists(settings_update.source_folder)
        if settings_update.default_publication_site is not None:
            current_settings.default_publication_site = settings_update.default_publication_site
        
        # Update Google Cloud Imagen fields
        if settings_update.google_cloud_project is not None:
            current_settings.google_cloud_project = settings_update.google_cloud_project
        if settings_update.google_cloud_location is not None:
            current_settings.google_cloud_location = settings_update.google_cloud_location
        if settings_update.google_cloud_credentials_path is not None:
            current_settings.google_cloud_credentials_path = settings_update.google_cloud_credentials_path
        if settings_update.imagen_enabled is not None:
            current_settings.imagen_enabled = settings_update.imagen_enabled
        if settings_update.imagen_model is not None:
            current_settings.imagen_model = settings_update.imagen_model
        
        current_settings.updated_at = datetime.now(timezone.utc)
        settings_db[SETTINGS_ID] = current_settings
        save_settings_to_file()  # Save to persistent storage
        
        # Return settings without sensitive data
        settings_data = current_settings.model_dump(mode='json')
        if settings_data.get("gemini_api_key"):
            settings_data["gemini_api_key"] = "***masked***"
        
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
            "gemini_api_key": bool(settings.gemini_api_key),
            "source_folder": bool(settings.source_folder),
            "source_folder_exists": False
        }
        
        # Check if source folder exists
        if settings.source_folder:
            validation_results["source_folder_exists"] = Path(settings.source_folder).exists()
        
        is_valid = all([
            validation_results["gemini_api_key"],
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

@app.post("/settings/test-gemini", response_model=APIResponse)
async def test_gemini_connection():
    """Test Gemini AI connection with current API key."""
    try:
        settings = settings_db.get(SETTINGS_ID)
        if not settings or not settings.gemini_api_key:
            raise HTTPException(status_code=400, detail="Gemini API key not configured")
        
        try:
            import google.generativeai as genai
            
            # Configure Gemini with the current API key
            genai.configure(api_key=settings.gemini_api_key)
            
            # Use the updated model name - gemini-1.5-flash is the current model
            model = genai.GenerativeModel('gemini-2.0-flash')
            response = model.generate_content("Say 'Hello, Gemini is working!' in a friendly way")
            
            return APIResponse(
                success=True,
                message="Gemini AI connection successful",
                data={"test_response": response.text}
            )
            
        except Exception as gemini_error:
            error_message = str(gemini_error)
            print(f"Gemini API Error Details: {error_message}")  # Add detailed logging
            return APIResponse(
                success=False,
                message="Gemini AI connection failed",
                data={"error": error_message, "error_type": type(gemini_error).__name__}
            )
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/settings/test-imagen", response_model=APIResponse)
async def test_imagen_connection():
    """Test Google Cloud Imagen API connection."""
    try:
        settings = settings_db.get(SETTINGS_ID)
        if not settings:
            raise HTTPException(status_code=404, detail="Settings not found")
        
        # Check if Imagen is enabled
        if not getattr(settings, 'imagen_enabled', False):
            return APIResponse(
                success=False,
                message="Imagen API is disabled in settings",
                data={"error": "Imagen disabled", "error_type": "configuration"}
            )
        
        # Check required configuration
        project_id = getattr(settings, 'google_cloud_project', None)
        location = getattr(settings, 'google_cloud_location', 'us-central1')
        credentials_path = getattr(settings, 'google_cloud_credentials_path', None)
        
        if not project_id:
            return APIResponse(
                success=False,
                message="Google Cloud project ID not configured",
                data={"error": "Missing project ID", "error_type": "configuration"}
            )
        
        # Try to import and test Google Cloud AI Platform
        try:
            from google.cloud import aiplatform
            import os
            
            # Set up authentication if credentials path is provided
            if credentials_path and os.path.exists(credentials_path):
                os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = credentials_path
            
            # Initialize the AI Platform client
            aiplatform.init(project=project_id, location=location)
            
            return APIResponse(
                success=True,
                message=f"Google Cloud Imagen API accessible (Project: {project_id}, Location: {location})",
                data={
                    "project_id": project_id,
                    "location": location,
                    "credentials_configured": bool(credentials_path and os.path.exists(credentials_path)),
                    "model": getattr(settings, 'imagen_model', 'imagen-3')
                }
            )
            
        except ImportError:
            return APIResponse(
                success=False,
                message="Google Cloud AI Platform library not installed",
                data={"error": "Missing google-cloud-aiplatform package", "error_type": "dependency"}
            )
        except Exception as e:
            return APIResponse(
                success=False,
                message="Failed to connect to Google Cloud Imagen API",
                data={"error": str(e), "error_type": type(e).__name__}
            )
            
    except HTTPException:
        raise
    except Exception as e:
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
