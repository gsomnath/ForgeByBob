from fastapi import FastAPI, HTTPException, Depends
from contextlib import asynccontextmanager

# Prevent Google Generative AI from auto-detecting Vertex AI
import os
_original_google_cloud_project = os.environ.get('GOOGLE_CLOUD_PROJECT')
os.environ.pop('GOOGLE_CLOUD_PROJECT', None)

import google.generativeai as genai

# Restore the original environment variable for Imagen
if _original_google_cloud_project:
    os.environ['GOOGLE_CLOUD_PROJECT'] = _original_google_cloud_project
try:
    from google.cloud import aiplatform
    IMAGEN_AVAILABLE = True
except ImportError:
    IMAGEN_AVAILABLE = False
    print("Warning: Google Cloud AI Platform not available. Image generation will use placeholders.")
import httpx
from typing import List, Optional
from pathlib import Path
import sys
import json
import base64
import hashlib
import uuid
from datetime import datetime, timezone

# Add the project root to the Python path
project_root = Path(__file__).parent.parent.parent
sys.path.append(str(project_root))

from shared.config import settings
from shared.models import (
    Blog, BlogCreate, BlogUpdate, BlogVersion, Comment, CommentCreate,
    APIResponse, BlogStatus, GeminiAPILog, ImagenAPILog
)
from shared.utils import (
    generate_id, get_current_timestamp, create_blog_folder_structure, save_blog_version,
    save_prompt, get_next_version_number, list_blog_versions,
    read_file_content, ensure_directory_exists
)

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Manage application lifecycle."""
    ensure_directory_exists(settings.source_folder)
    ensure_data_directory()
    load_blogs_from_file()
    load_comments_from_file()
    load_gemini_logs_from_file()
    load_imagen_logs_from_file()
    await configure_imagen()
    yield


app = FastAPI(
    title="Blog Service",
    description="Microservice for blog content management and AI generation",
    version="1.0.0",
    lifespan=lifespan
)

# Configure Gemini AI
async def get_current_api_key():
    """Get current API key from settings service."""
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{settings.settings_service_url}/settings/raw")
            if response.status_code == 200:
                data = response.json()
                if data.get("success") and data.get("data"):
                    return data["data"].get("gemini_api_key")
    except:
        pass
    return settings.gemini_api_key  # Fallback to environment

async def get_current_settings():
    """Get all current settings from settings service."""
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{settings.settings_service_url}/settings/raw", timeout=5.0)
            if response.status_code == 200:
                data = response.json()
                if data.get("success") and data.get("data"):
                    return data["data"]
    except Exception as e:
        print(f"Warning: Settings service exception: {e}")
    return None

async def configure_gemini_dynamic(api_key: str = None):
    """Configure Gemini AI with dynamic API key."""
    if not api_key:
        api_key = await get_current_api_key()
    
    if api_key:
        genai.configure(api_key=api_key)
        return True
    return False

# Imagen configuration
async def configure_imagen():
    """Configure Google Cloud Imagen API."""
    if not IMAGEN_AVAILABLE:
        print("Imagen not available - using placeholder image generation")
        return False
        
    try:
        # Get settings from database
        current_settings = await get_current_settings()
        
        # Handle both nested and flat settings structures
        if current_settings:
            # If we have main_settings key (nested structure)
            if 'main_settings' in current_settings:
                main_settings = current_settings['main_settings']
            else:
                # If it's already the flat settings structure
                main_settings = current_settings
        else:
            main_settings = None
            
        if not main_settings:
            print("Warning: No settings found. Imagen will use placeholders.")
            return False
            
        project_id = main_settings.get("google_cloud_project")
        location = main_settings.get("google_cloud_location", "us-central1")
        credentials_path = main_settings.get("google_cloud_credentials_path")
        
        if project_id and credentials_path:
            # Set environment variables for Google Cloud authentication
            os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = credentials_path
            os.environ['GOOGLE_CLOUD_PROJECT'] = project_id
            
            aiplatform.init(project=project_id, location=location)
            print(f"Imagen configured: project={project_id}, location={location}")
            return True
        else:
            missing = []
            if not project_id:
                missing.append("google_cloud_project")
            if not credentials_path:
                missing.append("google_cloud_credentials_path")
            print(f"Warning: Missing Google Cloud settings: {', '.join(missing)}. Imagen will use placeholders.")
            return False
    except Exception as e:
        print(f"Warning: Failed to configure Imagen: {e}")
        return False

async def generate_image_prompts_with_gemini(content: str, blog_title: str, user_prompt: str = "") -> List[str]:
    """Use Gemini API to generate high-quality image prompts based on blog content."""
    try:
        # Get current API key
        api_key = await get_current_api_key()
        if not api_key:
            # Fallback to default prompts
            return [
                f"Professional illustration related to {blog_title}, clean modern style, high quality, detailed artwork",
                f"Abstract representation of {blog_title} concept, minimalist design, professional quality"
            ]
        
        # Configure Gemini
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-2.0-flash')
        
        # Include user prompt if provided
        user_prompt_context = ""
        if user_prompt:
            user_prompt_context = f"""

Additional User Requirements for Images: {user_prompt}
Please incorporate these requirements into the image prompts where relevant.
"""
        
        # Create a prompt for Gemini to generate image descriptions
        gemini_prompt = f"""
Based on this blog post title and content, create 2 detailed, high-quality image generation prompts that would create visually appealing images to accompany the article.

Blog Title: {blog_title}

Blog Content Excerpt: {content[:1000]}...{user_prompt_context}

Requirements for each image prompt:
- Professional, high-quality visual style
- Relevant to the blog content themes
- Descriptive enough for AI image generation
- Avoid text/words in images
- Modern, clean aesthetic
- Each prompt should be different and complementary

Please provide exactly 2 image prompts, each on a separate line, starting with "Image 1:" and "Image 2:"
"""

        # Generate prompts using Gemini
        response = model.generate_content(gemini_prompt)
        generated_text = response.text.strip()
        
        # Parse the generated prompts
        image_prompts = []
        lines = generated_text.split('\n')
        
        for line in lines:
            line = line.strip()
            if line.startswith("Image 1:"):
                image_prompts.append(line.replace("Image 1:", "").strip())
            elif line.startswith("Image 2:"):
                image_prompts.append(line.replace("Image 2:", "").strip())
        
        # Ensure we have exactly 2 prompts
        if len(image_prompts) < 2:
            # Fallback if parsing failed
            image_prompts = [
                f"Professional illustration related to {blog_title}, clean modern style, high quality, detailed artwork",
                f"Abstract representation of {blog_title} concept, minimalist design, professional quality"
            ]
        
        return image_prompts[:2]  # Ensure exactly 2 prompts
        
    except Exception as e:
        print(f"Error generating image prompts with Gemini: {e}")
        # Fallback to default prompts
        return [
            f"Professional illustration related to {blog_title}, clean modern style, high quality, detailed artwork",
            f"Abstract representation of {blog_title} concept, minimalist design, professional quality"
        ]

def generate_static_image_url(blog_id: str, image_number: int) -> str:
    """Generate a static image URL that won't change on page refresh."""
    seed = f"{blog_id}_{image_number}"
    hash_value = hashlib.md5(seed.encode()).hexdigest()
    image_id = int(hash_value[:6], 16) % 1000 + 1
    return f"https://picsum.photos/id/{image_id}/800/600"

def save_imagen_response_to_file(imagen_response, blog_id: str, image_number: int) -> str:
    """Save Imagen API response image to local file and return the URL."""
    try:
        # Create images directory if it doesn't exist
        images_dir = Path("generated_images")
        images_dir.mkdir(exist_ok=True)
        
        # Create filename with blog_id and image number
        filename = f"{blog_id}_image_{image_number}_{uuid.uuid4().hex[:8]}.png"
        file_path = images_dir / filename
        
        # Get the first image from the response
        if imagen_response.images and len(imagen_response.images) > 0:
            image = imagen_response.images[0]
            
            # Save the image to file
            with open(file_path, "wb") as f:
                f.write(image._image_bytes)
            
            # Return local URL that will be served by UI service
            return f"http://localhost:8003/images/{filename}"
        
        return None
    except Exception as e:
        print(f"Error saving Imagen response to file: {e}")
        return None

async def generate_images_with_imagen(content: str, blog_title: str, blog_id: str, user_prompt: str = "") -> List[str]:
    """Generate 2 images based on blog content using Imagen."""
    try:
        # Use Gemini to generate high-quality image prompts
        image_prompts = await generate_image_prompts_with_gemini(content, blog_title, user_prompt)
        
        generated_images = []
        
        # Try to use actual Imagen API if available
        if IMAGEN_AVAILABLE:
            try:
                # Get current settings from settings service
                current_settings = await get_current_settings()
                
                # Handle both nested and flat settings structures
                if current_settings:
                    # If we have main_settings key (nested structure)
                    if 'main_settings' in current_settings:
                        main_settings = current_settings['main_settings']
                    else:
                        # If it's already the flat settings structure
                        main_settings = current_settings
                else:
                    main_settings = None
                
                if not main_settings:
                    print("Warning: No settings found for Imagen")
                    # Use fallback placeholder images
                    for i, prompt in enumerate(image_prompts, 1):
                        start_time = get_current_timestamp()
                        log_id = log_imagen_request(blog_id, f"Image {i}: {prompt}", "no-settings-fallback")
                        
                        placeholder_url = generate_static_image_url(blog_id, i)
                        generated_images.append(placeholder_url)
                        
                        end_time = get_current_timestamp()
                        processing_time_ms = int((end_time - start_time).total_seconds() * 1000)
                        log_imagen_response(log_id, [placeholder_url], "No settings found, using placeholder", processing_time_ms)
                    return generated_images
                
                project_id = main_settings.get("google_cloud_project")
                location = main_settings.get("google_cloud_location", "us-central1")
                credentials_path = main_settings.get("google_cloud_credentials_path")
                imagen_enabled = main_settings.get("imagen_enabled", False)
                imagen_model = main_settings.get("imagen_model", "imagen-3")
                
                if project_id and imagen_enabled:
                    # Set up authentication if credentials path is provided
                    if credentials_path and os.path.exists(credentials_path):
                        os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = credentials_path
                    
                    # Log each image generation request
                    for i, prompt in enumerate(image_prompts, 1):
                        start_time = get_current_timestamp()
                        log_id = log_imagen_request(blog_id, f"Image {i}: {prompt}", imagen_model)
                        
                        try:
                            # Set up authentication
                            google_cloud_credentials = main_settings.get("google_cloud_credentials_path")
                            if google_cloud_credentials:
                                os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = google_cloud_credentials
                            
                            # Initialize Vertex AI
                            import vertexai
                            from vertexai.preview.vision_models import ImageGenerationModel
                            
                            vertexai.init(project=project_id, location=location)
                            
                            # Get the image generation model
                            model = ImageGenerationModel.from_pretrained(imagen_model)
                            
                            # Generate images
                            response = model.generate_images(
                                prompt=prompt,
                                number_of_images=1,
                                language="en",
                                aspect_ratio="1:1"
                            )
                            
                            if response and response.images:
                                # Save the actual Imagen-generated image to local file
                                image_url = save_imagen_response_to_file(response, blog_id, i)
                                
                                if image_url:
                                    generated_images.append(image_url)
                                    # Log successful response with real image URL
                                    end_time = get_current_timestamp()
                                    processing_time_ms = int((end_time - start_time).total_seconds() * 1000)
                                    log_imagen_response(log_id, [image_url], f"Successfully generated and saved with Imagen {imagen_model}", processing_time_ms)
                                else:
                                    # Fallback if saving failed
                                    fallback_url = generate_static_image_url(blog_id, i)
                                    generated_images.append(fallback_url)
                                    end_time = get_current_timestamp()
                                    processing_time_ms = int((end_time - start_time).total_seconds() * 1000)
                                    log_imagen_response(log_id, [fallback_url], "Imagen generated but save failed, using fallback", processing_time_ms)
                            else:
                                # Fallback to placeholder
                                placeholder_url = generate_static_image_url(blog_id, i)
                                generated_images.append(placeholder_url)
                                
                                # Log as fallback
                                end_time = get_current_timestamp()
                                processing_time_ms = int((end_time - start_time).total_seconds() * 1000)
                                log_imagen_response(log_id, [placeholder_url], "No images generated by Imagen API", processing_time_ms)
                                
                        except Exception as api_error:
                            # Log API error and use placeholder
                            placeholder_url = generate_static_image_url(blog_id, i)
                            generated_images.append(placeholder_url)
                            
                            end_time = get_current_timestamp()
                            processing_time_ms = int((end_time - start_time).total_seconds() * 1000)
                            log_imagen_response(log_id, [placeholder_url], f"Imagen API error: {str(api_error)}", processing_time_ms)
                            print(f"Imagen API error for prompt '{prompt}': {api_error}")
                else:
                    # No project ID or Imagen not enabled, log and use placeholders
                    fallback_reason = "Imagen not enabled" if not imagen_enabled else "Google Cloud project not configured"
                    imagen_model = current_settings.get("imagen_model", "imagen-3") if current_settings else "imagen-3"
                    for i, prompt in enumerate(image_prompts, 1):
                        start_time = get_current_timestamp()
                        log_id = log_imagen_request(blog_id, f"Image {i}: {prompt}", f"{imagen_model}-fallback")
                        
                        placeholder_url = generate_static_image_url(blog_id, i)
                        generated_images.append(placeholder_url)
                        
                        end_time = get_current_timestamp()
                        processing_time_ms = int((end_time - start_time).total_seconds() * 1000)
                        log_imagen_response(log_id, [placeholder_url], f"{fallback_reason}, using placeholder", processing_time_ms)
            
            except Exception as setup_error:
                print(f"Imagen setup error: {setup_error}")
                # Fallback to placeholder with logging
                for i, prompt in enumerate(image_prompts, 1):
                    start_time = get_current_timestamp()
                    log_id = log_imagen_request(blog_id, f"Image {i}: {prompt}", "imagen-3-error")
                    
                    placeholder_url = generate_static_image_url(blog_id, i)
                    generated_images.append(placeholder_url)
                    
                    end_time = get_current_timestamp()
                    processing_time_ms = int((end_time - start_time).total_seconds() * 1000)
                    log_imagen_response(log_id, [placeholder_url], f"Imagen setup error: {str(setup_error)}", processing_time_ms)
        else:
            # Imagen not available, log and use placeholders
            for i, prompt in enumerate(image_prompts, 1):
                start_time = get_current_timestamp()
                log_id = log_imagen_request(blog_id, f"Image {i}: {prompt}", "placeholder-service")
                
                placeholder_url = generate_static_image_url(blog_id, i)
                generated_images.append(placeholder_url)
                
                end_time = get_current_timestamp()
                processing_time_ms = int((end_time - start_time).total_seconds() * 1000)
                log_imagen_response(log_id, [placeholder_url], "Imagen package not available, using placeholder service", processing_time_ms)
        
        return generated_images
        
    except Exception as e:
        print(f"Error generating images with Imagen: {e}")
        # Emergency fallback to static placeholder images with basic logging
        fallback_images = [
            generate_static_image_url(blog_id, 1),
            generate_static_image_url(blog_id, 2)
        ]
        
        # Log the fallback
        try:
            log_id = log_imagen_request(blog_id, f"Emergency fallback for {blog_title}", "fallback-service")
            log_imagen_response(log_id, fallback_images, f"Emergency fallback due to error: {str(e)}", 0)
        except:
            pass  # Don't let logging errors prevent fallback
            
        return fallback_images

# Persistent storage paths
DATA_DIR = Path("data")
BLOGS_DB_FILE = DATA_DIR / "blogs.json"
COMMENTS_DB_FILE = DATA_DIR / "comments.json"
GEMINI_LOGS_FILE = DATA_DIR / "gemini_logs.json"
IMAGEN_LOGS_FILE = DATA_DIR / "imagen_logs.json"

# In-memory storage (loaded from persistent storage)
blogs_db = {}
comments_db = {}
gemini_logs = []  # List to store API logs, ordered by timestamp
imagen_logs = []  # List to store Imagen API logs, ordered by timestamp

def ensure_data_directory():
    """Ensure data directory exists."""
    DATA_DIR.mkdir(exist_ok=True)

def load_blogs_from_file():
    """Load blogs from persistent storage."""
    global blogs_db
    try:
        if BLOGS_DB_FILE.exists():
            with open(BLOGS_DB_FILE, 'r', encoding='utf-8') as f:
                data = json.load(f)
                # Convert back to Blog objects
                for blog_id, blog_data in data.items():
                    # Convert datetime strings back to datetime objects
                    if 'created_at' in blog_data:
                        blog_data['created_at'] = datetime.fromisoformat(blog_data['created_at'].replace('Z', '+00:00'))
                    if 'updated_at' in blog_data:
                        blog_data['updated_at'] = datetime.fromisoformat(blog_data['updated_at'].replace('Z', '+00:00'))
                    blogs_db[blog_id] = Blog(**blog_data)
                print(f"Loaded {len(blogs_db)} blogs from persistent storage")
    except Exception as e:
        print(f"Error loading blogs from file: {e}")
        blogs_db = {}

def save_blogs_to_file():
    """Save blogs to persistent storage."""
    try:
        ensure_data_directory()
        # Convert Blog objects to serializable dict
        data = {}
        for blog_id, blog in blogs_db.items():
            blog_dict = blog.model_dump(mode='json')
            data[blog_id] = blog_dict
        
        with open(BLOGS_DB_FILE, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
    except Exception as e:
        print(f"Error saving blogs to file: {e}")

def load_comments_from_file():
    """Load comments from persistent storage."""
    global comments_db
    try:
        if COMMENTS_DB_FILE.exists():
            with open(COMMENTS_DB_FILE, 'r', encoding='utf-8') as f:
                data = json.load(f)
                # Convert back to Comment objects
                for blog_id, comments_list in data.items():
                    comments_db[blog_id] = []
                    for comment_data in comments_list:
                        # Convert datetime strings back to datetime objects
                        if 'created_at' in comment_data:
                            comment_data['created_at'] = datetime.fromisoformat(comment_data['created_at'].replace('Z', '+00:00'))
                        comments_db[blog_id].append(Comment(**comment_data))
                print(f"Loaded comments for {len(comments_db)} blogs from persistent storage")
    except Exception as e:
        print(f"Error loading comments from file: {e}")
        comments_db = {}

def save_comments_to_file():
    """Save comments to persistent storage."""
    try:
        ensure_data_directory()
        # Convert Comment objects to serializable dict
        data = {}
        for blog_id, comments_list in comments_db.items():
            data[blog_id] = [comment.model_dump(mode='json') for comment in comments_list]
        
        with open(COMMENTS_DB_FILE, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
    except Exception as e:
        print(f"Error saving comments to file: {e}")

def load_gemini_logs_from_file():
    """Load Gemini API logs from persistent storage."""
    global gemini_logs
    try:
        if GEMINI_LOGS_FILE.exists():
            with open(GEMINI_LOGS_FILE, 'r', encoding='utf-8') as f:
                data = json.load(f)
                gemini_logs = []
                for log_data in data:
                    # Convert datetime strings back to datetime objects
                    if 'request_timestamp' in log_data:
                        log_data['request_timestamp'] = datetime.fromisoformat(log_data['request_timestamp'].replace('Z', '+00:00'))
                    if 'response_timestamp' in log_data and log_data['response_timestamp']:
                        log_data['response_timestamp'] = datetime.fromisoformat(log_data['response_timestamp'].replace('Z', '+00:00'))
                    gemini_logs.append(GeminiAPILog(**log_data))
                # Sort by timestamp (newest first)
                gemini_logs.sort(key=lambda x: x.request_timestamp, reverse=True)
                # Keep only last 200 logs
                gemini_logs = gemini_logs[:200]
                print(f"Loaded {len(gemini_logs)} Gemini API logs from persistent storage")
    except Exception as e:
        print(f"Error loading Gemini logs from file: {e}")
        gemini_logs = []

def save_gemini_logs_to_file():
    """Save Gemini API logs to persistent storage."""
    try:
        ensure_data_directory()
        # Keep only last 200 logs
        logs_to_save = gemini_logs[:200]
        # Convert to serializable dict
        data = [log.model_dump(mode='json') for log in logs_to_save]
        
        with open(GEMINI_LOGS_FILE, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
    except Exception as e:
        print(f"Error saving Gemini logs to file: {e}")

def log_gemini_request(blog_id: str, prompt: str, model_used: str = "gemini-2.0-flash"):
    """Log a Gemini API request."""
    global gemini_logs
    log_entry = GeminiAPILog(
        id=generate_id(),
        request_timestamp=get_current_timestamp(),
        blog_id=blog_id,
        prompt=prompt,
        model_used=model_used,
        success=False  # Will be updated when response is received
    )
    gemini_logs.insert(0, log_entry)  # Add to beginning (newest first)
    return log_entry.id

def log_gemini_response(log_id: str, response_content: str = None, error_message: str = None, processing_time_ms: int = None):
    """Update a Gemini API log with response information."""
    global gemini_logs
    for log_entry in gemini_logs:
        if log_entry.id == log_id:
            log_entry.response_timestamp = get_current_timestamp()
            log_entry.response_content = response_content
            log_entry.error_message = error_message
            log_entry.processing_time_ms = processing_time_ms
            log_entry.success = response_content is not None
            break
    
    # Keep only last 200 logs
    gemini_logs = gemini_logs[:200]
    save_gemini_logs_to_file()

def load_imagen_logs_from_file():
    """Load Imagen API logs from persistent storage."""
    global imagen_logs
    try:
        if IMAGEN_LOGS_FILE.exists():
            with open(IMAGEN_LOGS_FILE, 'r', encoding='utf-8') as f:
                data = json.load(f)
                imagen_logs = []
                for log_data in data:
                    # Convert datetime strings back to datetime objects
                    if 'request_timestamp' in log_data:
                        log_data['request_timestamp'] = datetime.fromisoformat(log_data['request_timestamp'].replace('Z', '+00:00'))
                    if 'response_timestamp' in log_data and log_data['response_timestamp']:
                        log_data['response_timestamp'] = datetime.fromisoformat(log_data['response_timestamp'].replace('Z', '+00:00'))
                    imagen_logs.append(ImagenAPILog(**log_data))
                # Sort by timestamp (newest first)
                imagen_logs.sort(key=lambda x: x.request_timestamp, reverse=True)
                # Keep only last 200 logs
                imagen_logs = imagen_logs[:200]
                print(f"Loaded {len(imagen_logs)} Imagen API logs from persistent storage")
    except Exception as e:
        print(f"Error loading Imagen logs from file: {e}")
        imagen_logs = []

def save_imagen_logs_to_file():
    """Save Imagen API logs to persistent storage."""
    try:
        ensure_data_directory()
        # Keep only last 200 logs
        logs_to_save = imagen_logs[:200]
        # Convert to serializable dict
        data = [log.model_dump(mode='json') for log in logs_to_save]
        
        with open(IMAGEN_LOGS_FILE, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
    except Exception as e:
        print(f"Error saving Imagen logs to file: {e}")

def log_imagen_request(blog_id: str, prompt: str, model_used: str = "imagen-3"):
    """Log an Imagen API request."""
    global imagen_logs
    log_entry = ImagenAPILog(
        id=generate_id(),
        request_timestamp=get_current_timestamp(),
        blog_id=blog_id,
        prompt=prompt,
        model_used=model_used,
        success=False  # Will be updated when response is received
    )
    imagen_logs.insert(0, log_entry)  # Add to beginning (newest first)
    return log_entry.id

def log_imagen_response(log_id: str, image_urls: List[str] = None, error_message: str = None, processing_time_ms: int = None):
    """Update an Imagen API log with response information."""
    global imagen_logs
    for log_entry in imagen_logs:
        if log_entry.id == log_id:
            log_entry.response_timestamp = get_current_timestamp()
            log_entry.image_urls = image_urls
            log_entry.error_message = error_message
            log_entry.processing_time_ms = processing_time_ms
            log_entry.success = image_urls is not None and len(image_urls) > 0
            break
    
    # Keep only last 200 logs
    imagen_logs = imagen_logs[:200]
    save_imagen_logs_to_file()

def clear_imagen_logs_for_blog(blog_id: str):
    """Clear all existing Imagen logs for a specific blog ID to avoid confusion."""
    global imagen_logs
    imagen_logs = [log for log in imagen_logs if log.blog_id != blog_id]
    save_imagen_logs_to_file()


@app.get("/")
async def root():
    """Root endpoint."""
    return APIResponse(
        success=True,
        message="Blog Service is running",
        data={"version": "1.0.0"}
    )

@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "service": "blog-service"}

@app.get("/gemini-logs", response_model=APIResponse)
async def get_gemini_logs(page: int = 1, page_size: int = 10):
    """Get Gemini API logs with pagination."""
    try:
        # Calculate pagination
        total_logs = len(gemini_logs)
        start_idx = (page - 1) * page_size
        end_idx = start_idx + page_size
        
        # Get logs for current page
        page_logs = gemini_logs[start_idx:end_idx]
        logs_data = [log.model_dump(mode='json') for log in page_logs]
        
        # Calculate pagination info
        total_pages = (total_logs + page_size - 1) // page_size
        
        return APIResponse(
            success=True,
            message="Gemini logs retrieved successfully",
            data={
                "logs": logs_data,
                "pagination": {
                    "current_page": page,
                    "page_size": page_size,
                    "total_logs": total_logs,
                    "total_pages": total_pages,
                    "has_next": page < total_pages,
                    "has_prev": page > 1
                }
            }
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/imagen-logs", response_model=APIResponse)
async def get_imagen_logs(page: int = 1, page_size: int = 10):
    """Get Imagen API logs with pagination."""
    try:
        # Calculate pagination
        total_logs = len(imagen_logs)
        start_idx = (page - 1) * page_size
        end_idx = start_idx + page_size
        
        # Get logs for current page
        page_logs = imagen_logs[start_idx:end_idx]
        logs_data = [log.model_dump(mode='json') for log in page_logs]
        
        # Calculate pagination info
        total_pages = (total_logs + page_size - 1) // page_size
        
        return APIResponse(
            success=True,
            message="Imagen logs retrieved successfully",
            data={
                "logs": logs_data,
                "pagination": {
                    "current_page": page,
                    "page_size": page_size,
                    "total_logs": total_logs,
                    "total_pages": total_pages,
                    "has_next": page < total_pages,
                    "has_prev": page > 1
                }
            }
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/blogs", response_model=APIResponse)
async def create_blog(blog_data: BlogCreate):
    """Create a new blog."""
    try:
        blog_id = generate_id()
        
        # Create folder structure
        folder_path = create_blog_folder_structure(settings.source_folder, blog_data.title)
        
        # Save initial prompt
        save_prompt(folder_path, blog_data.initial_prompt, "initial_prompt.txt")
        
        # Create blog record
        blog = Blog(
            id=blog_id,
            title=blog_data.title,
            description=blog_data.description,
            tags=blog_data.tags,
            publication_site=blog_data.publication_site,
            status=BlogStatus.DRAFT,
            created_at=get_current_timestamp(),
            updated_at=get_current_timestamp(),
            folder_path=folder_path,
            current_version=0
        )
        
        blogs_db[blog_id] = blog
        save_blogs_to_file()  # Save to persistent storage
        
        return APIResponse(
            success=True,
            message="Blog created successfully",
            data=blog.model_dump(mode='json')
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/blogs", response_model=APIResponse)
async def get_blogs():
    """Get all blogs."""
    try:
        blogs_list = [blog.model_dump(mode='json') for blog in blogs_db.values()]
        return APIResponse(
            success=True,
            message="Blogs retrieved successfully",
            data=blogs_list
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/blogs/{blog_id}", response_model=APIResponse)
async def get_blog(blog_id: str):
    """Get a specific blog."""
    try:
        if blog_id not in blogs_db:
            raise HTTPException(status_code=404, detail="Blog not found")
        
        blog = blogs_db[blog_id]
        return APIResponse(
            success=True,
            message="Blog retrieved successfully",
            data=blog.model_dump(mode='json')
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.put("/blogs/{blog_id}", response_model=APIResponse)
async def update_blog(blog_id: str, blog_update: BlogUpdate):
    """Update a blog."""
    try:
        if blog_id not in blogs_db:
            raise HTTPException(status_code=404, detail="Blog not found")
        
        blog = blogs_db[blog_id]
        
        # Update fields
        if blog_update.title is not None:
            blog.title = blog_update.title
        if blog_update.description is not None:
            blog.description = blog_update.description
        if blog_update.tags is not None:
            blog.tags = blog_update.tags
        if blog_update.publication_site is not None:
            blog.publication_site = blog_update.publication_site
        if blog_update.status is not None:
            blog.status = blog_update.status
        
        blog.updated_at = get_current_timestamp()
        save_blogs_to_file()  # Save to persistent storage
        
        return APIResponse(
            success=True,
            message="Blog updated successfully",
            data=blog.model_dump(mode='json')
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/blogs/{blog_id}", response_model=APIResponse)
async def delete_blog(blog_id: str):
    """Delete a blog."""
    try:
        if blog_id not in blogs_db:
            raise HTTPException(status_code=404, detail="Blog not found")
        
        del blogs_db[blog_id]
        save_blogs_to_file()  # Save to persistent storage
        
        return APIResponse(
            success=True,
            message="Blog deleted successfully"
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/blogs/{blog_id}/versions", response_model=APIResponse)
async def get_blog_versions(blog_id: str):
    """Get all versions of a blog."""
    try:
        if blog_id not in blogs_db:
            raise HTTPException(status_code=404, detail="Blog not found")
        
        blog = blogs_db[blog_id]
        versions = list_blog_versions(blog.folder_path)
        
        return APIResponse(
            success=True,
            message="Blog versions retrieved successfully",
            data=versions
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/blogs/{blog_id}/versions/{version_num}/content", response_model=APIResponse)
async def get_blog_version_content(blog_id: str, version_num: int):
    """Get the content of a specific blog version."""
    try:
        if blog_id not in blogs_db:
            raise HTTPException(status_code=404, detail="Blog not found")
        
        blog = blogs_db[blog_id]
        final_folder = Path(blog.folder_path) / "final"
        version_file = final_folder / f"v{version_num}.md"
        
        if not version_file.exists():
            raise HTTPException(status_code=404, detail="Version not found")
        
        with open(version_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        return APIResponse(
            success=True,
            message="Version content retrieved successfully",
            data={"content": content}
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.put("/blogs/{blog_id}/content", response_model=APIResponse)
async def update_blog_content(blog_id: str, content_data: dict):
    """Update blog content manually."""
    try:
        if blog_id not in blogs_db:
            raise HTTPException(status_code=404, detail="Blog not found")
        
        blog = blogs_db[blog_id]
        new_content = content_data.get("content", "")
        
        if not new_content.strip():
            raise HTTPException(status_code=400, detail="Content cannot be empty")
        
        # Save as new version if this is different from current content
        if blog.latest_content != new_content:
            # Get next version number and save content
            version_number = get_next_version_number(blog.folder_path)
            version_file = save_blog_version(blog.folder_path, new_content, version_number)
            
            # Update blog with new content
            blog.current_version = version_number
            blog.latest_content = new_content
            blog.updated_at = get_current_timestamp()
            blog.status = BlogStatus.IN_PROGRESS
            save_blogs_to_file()  # Save to persistent storage
            
            return APIResponse(
                success=True,
                message="Blog content updated successfully",
                data={
                    "version": version_number,
                    "content": new_content,
                    "file_path": version_file
                }
            )
        else:
            return APIResponse(
                success=True,
                message="No changes detected",
                data={
                    "version": blog.current_version,
                    "content": blog.latest_content
                }
            )
            
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/blogs/{blog_id}/versions/{version_num}", response_model=APIResponse)
async def delete_blog_version(blog_id: str, version_num: int):
    """Delete a specific blog version."""
    try:
        if blog_id not in blogs_db:
            raise HTTPException(status_code=404, detail="Blog not found")
        
        blog = blogs_db[blog_id]
        final_folder = Path(blog.folder_path) / "final"
        version_file = final_folder / f"v{version_num}.md"
        
        if not version_file.exists():
            raise HTTPException(status_code=404, detail="Version not found")
        
        # Don't allow deleting the current/latest version
        if version_num == blog.current_version:
            raise HTTPException(status_code=400, detail="Cannot delete the current version. Please create a new version first.")
        
        # Delete the version file
        version_file.unlink()
        
        # If this was the latest content and we're deleting it, update to the highest remaining version
        remaining_versions = list_blog_versions(blog.folder_path)
        if remaining_versions:
            # Find the highest version number
            highest_version = max(v["version"] for v in remaining_versions)
            if blog.current_version == version_num or blog.current_version > highest_version:
                # Update to the highest remaining version
                blog.current_version = highest_version
                # Load the content from the highest remaining version
                highest_version_file = final_folder / f"v{highest_version}.md"
                if highest_version_file.exists():
                    with open(highest_version_file, 'r', encoding='utf-8') as f:
                        blog.latest_content = f.read()
                blog.updated_at = get_current_timestamp()
                save_blogs_to_file()
        
        return APIResponse(
            success=True,
            message=f"Version {version_num} deleted successfully",
            data={"deleted_version": version_num, "current_version": blog.current_version}
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/blogs/{blog_id}/generate", response_model=APIResponse)
async def generate_blog_content(blog_id: str, request_data: dict):
    """Generate new blog content using Gemini AI."""
    try:
        if blog_id not in blogs_db:
            raise HTTPException(status_code=404, detail="Blog not found")
        
        blog = blogs_db[blog_id]
        prompt = request_data.get("prompt", "")
        generation_type = request_data.get("generation_type", "all")  # all, text, images
        
        if not prompt:
            raise HTTPException(status_code=400, detail="Prompt is required")
            
        # Validate generation type
        if generation_type not in ["all", "text", "images"]:
            raise HTTPException(status_code=400, detail="Invalid generation_type. Must be 'all', 'text', or 'images'")
        
        # For image-only generation, we need existing content
        if generation_type == "images" and not blog.latest_content:
            raise HTTPException(status_code=400, detail="Cannot generate images only without existing text content")
        
        # Get current API key from settings service
        current_api_key = await get_current_api_key()
        if not current_api_key:
            raise HTTPException(status_code=500, detail="Gemini API key not configured")
        
        try:
            final_content = ""
            images_generated = False
            text_generated = False
            log_id = None
            start_time = None
            
            # Handle different generation types
            if generation_type in ["all", "text"]:
                # Generate text content
                current_content_context = ""
                if blog.latest_content:
                    current_content_context = f"""

Current Blog Content:
{blog.latest_content}

"""
                
                enhanced_prompt = f"""You are an expert blog writer creating high-quality, engaging content for the blog titled: "{blog.title}"
                
Blog Description: {blog.description or "No description provided"}
Tags: {', '.join(blog.tags) if blog.tags else "No tags"}
Publication Site: {blog.publication_site or "General audience"}{current_content_context}
User Request: {prompt}

IMPORTANT REQUIREMENTS:
1. Create professional, well-structured blog content that is engaging, informative, and optimized for the target audience
2. Use appropriate headings, bullet points, and formatting when relevant
3. Write in a clear, professional tone suitable for online publication
4. DO NOT include any images in your response - images will be generated separately
5. Focus purely on text content with excellent structure and flow
6. Create comprehensive, detailed content that stands on its own
7. Use markdown formatting for headers, lists, and emphasis

{f"Based on the current content above, " + prompt if blog.latest_content else prompt}"""
                
                # Log the request
                start_time = get_current_timestamp()
                log_id = log_gemini_request(blog_id, enhanced_prompt, 'gemini-2.0-flash')
                
                # Configure Gemini with current API key
                await configure_gemini_dynamic(current_api_key)
                
                # Initialize Gemini model
                model = genai.GenerativeModel('gemini-2.0-flash')
                
                # Generate content
                response = model.generate_content(enhanced_prompt)
                generated_content = response.text
                text_generated = True
                
                # Calculate processing time and log response
                end_time = get_current_timestamp()
                processing_time_ms = int((end_time - start_time).total_seconds() * 1000)
                log_gemini_response(log_id, generated_content, None, processing_time_ms)
            else:
                # For images-only generation, use existing content
                generated_content = blog.latest_content
            
            # Handle image generation
            if generation_type in ["all", "images"]:
                try:
                    image_urls = await generate_images_with_imagen(generated_content, blog.title, blog_id, prompt)
                    images_generated = True
                    
                    # Create the final content with images
                    if generation_type == "images":
                        # For images-only, replace existing image section or add at the end
                        content_lines = generated_content.split('\n')
                        
                        # Find and remove existing image section
                        start_idx = -1
                        for i, line in enumerate(content_lines):
                            if line.strip() == "## Generated Images":
                                start_idx = i
                                break
                        
                        if start_idx >= 0:
                            # Remove existing image section
                            content_lines = content_lines[:start_idx]
                        
                        # Add new image section
                        base_content = '\n'.join(content_lines).rstrip()
                        final_content = base_content + "\n\n---\n\n## Generated Images\n\n"
                    else:
                        # For all or text+images, add images to the generated content
                        final_content = generated_content + "\n\n---\n\n## Generated Images\n\n"
                    
                    final_content += "*The following images were generated based on the blog content and can be manually placed throughout the article as needed:*\n\n"
                    
                    for i, image_url in enumerate(image_urls, 1):
                        # Create descriptive alt text based on content themes
                        if "AI" in generated_content.upper() or "artificial intelligence" in generated_content.lower():
                            alt_text = f"AI and technology illustration {i}"
                        elif "coding" in generated_content.lower() or "development" in generated_content.lower():
                            alt_text = f"Software development illustration {i}"
                        else:
                            alt_text = f"Professional illustration related to {blog.title} - Image {i}"
                        
                        final_content += f"**Image {i}:**\n"
                        final_content += f"![{alt_text}]({image_url})\n\n"
                    
                except Exception as img_error:
                    print(f"Warning: Image generation failed: {img_error}")
                    images_generated = False
                    if generation_type == "images":
                        raise HTTPException(status_code=500, detail=f"Image generation failed: {str(img_error)}")
                    else:
                        # For all/text generation, continue without images
                        final_content = generated_content + "\n\n---\n\n*Note: Image generation was not available for this content.*"
            else:
                # Text-only generation
                final_content = generated_content
            
            # Save the prompt
            save_prompt(blog.folder_path, prompt)
            
            # Get next version number and save content
            version_number = get_next_version_number(blog.folder_path)
            version_file = save_blog_version(blog.folder_path, final_content, version_number)
            
            # Update blog with latest content
            blog.current_version = version_number
            blog.latest_content = final_content
            blog.updated_at = get_current_timestamp()
            blog.status = BlogStatus.IN_PROGRESS
            save_blogs_to_file()  # Save to persistent storage
            
            # Create success message based on generation type
            if generation_type == "text":
                message = "Blog text content generated successfully"
            elif generation_type == "images":
                message = "Blog images generated successfully"
            else:
                message = "Blog content generated successfully with text and images"
            
            return APIResponse(
                success=True,
                message=message,
                data={
                    "version": version_number,
                    "content": final_content,
                    "file_path": version_file,
                    "generation_type": generation_type,
                    "text_generated": text_generated,
                    "images_generated": images_generated
                }
            )
            
        except Exception as ai_error:
            if log_id and start_time:
                end_time = get_current_timestamp()
                processing_time_ms = int((end_time - start_time).total_seconds() * 1000)
                log_gemini_response(log_id, None, str(ai_error), processing_time_ms)
            raise HTTPException(status_code=500, detail=f"AI generation error: {str(ai_error)}")
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/blogs/{blog_id}/comments", response_model=APIResponse)
async def add_comment(blog_id: str, comment_data: CommentCreate):
    """Add a comment to a blog."""
    try:
        if blog_id not in blogs_db:
            raise HTTPException(status_code=404, detail="Blog not found")
        
        comment_id = generate_id()
        comment = Comment(
            id=comment_id,
            blog_id=blog_id,
            content=comment_data.content,
            requested_changes=comment_data.requested_changes,
            created_at=get_current_timestamp()
        )
        
        if blog_id not in comments_db:
            comments_db[blog_id] = []
        comments_db[blog_id].append(comment)
        save_comments_to_file()  # Save to persistent storage
        
        return APIResponse(
            success=True,
            message="Comment added successfully",
            data=comment.model_dump(mode='json')
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/blogs/{blog_id}/comments", response_model=APIResponse)
async def get_blog_comments(blog_id: str):
    """Get all comments for a blog."""
    try:
        if blog_id not in blogs_db:
            raise HTTPException(status_code=404, detail="Blog not found")
        
        comments = comments_db.get(blog_id, [])
        comments_list = [comment.model_dump(mode='json') for comment in comments]
        
        return APIResponse(
            success=True,
            message="Comments retrieved successfully",
            data=comments_list
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=settings.blog_service_port)
