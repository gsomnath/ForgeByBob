from fastapi import FastAPI, HTTPException, Depends
from contextlib import asynccontextmanager
import os
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
    APIResponse, BlogStatus, WatsonxAPILog
)
from shared.utils import (
    generate_id, get_current_timestamp, create_blog_folder_structure, save_blog_version,
    save_prompt, get_next_version_number, list_blog_versions,
    read_file_content, ensure_directory_exists
)

# Import IBM watsonx client
from services.watsonx_service.granite_client import get_granite_client

# Image generation will use placeholder images
IMAGEN_AVAILABLE = False

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Manage application lifecycle."""
    ensure_directory_exists(settings.source_folder)
    ensure_data_directory()
    load_blogs_from_file()
    load_comments_from_file()
    load_watsonx_logs_from_file()
    yield


app = FastAPI(
    title="Blog Service",
    description="Microservice for blog content management and AI generation",
    version="1.0.0",
    lifespan=lifespan
)

# IBM watsonx client (initialized globally)
watsonx_client = None

async def get_watsonx_client():
    """Get or initialize IBM watsonx client."""
    global watsonx_client
    if watsonx_client is None:
        watsonx_client = get_granite_client()
    return watsonx_client

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


async def generate_image_prompts_with_watsonx(content: str, blog_title: str, user_prompt: str = "") -> List[str]:
    """Use IBM watsonx.ai to generate high-quality image prompts based on blog content."""
    try:
        # Get watsonx client
        client = await get_watsonx_client()
        if not client:
            # Fallback to default prompts
            return [
                f"Professional illustration related to {blog_title}, clean modern style, high quality, detailed artwork",
                f"Abstract representation of {blog_title} concept, minimalist design, professional quality"
            ]
        
        # Include user prompt if provided
        user_prompt_context = ""
        if user_prompt:
            user_prompt_context = f"""

Additional User Requirements for Images: {user_prompt}
Please incorporate these requirements into the image prompts where relevant.
"""
        
        # Create a prompt for watsonx to generate image descriptions
        watsonx_prompt = f"""
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

        # Generate prompts using IBM watsonx
        response = client.generate(watsonx_prompt, max_tokens=500)
        generated_text = response.strip()
        
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
        print(f"Error generating image prompts with IBM watsonx: {e}")
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

async def generate_images_with_placeholder(content: str, blog_title: str, blog_id: str, user_prompt: str = "") -> List[str]:
    """Image generation is disabled. Returns empty list."""
    # Image generation functionality has been disabled
    return []

# Persistent storage paths
DATA_DIR = Path("data")
BLOGS_DB_FILE = DATA_DIR / "blogs.json"
COMMENTS_DB_FILE = DATA_DIR / "comments.json"
WATSONX_LOGS_FILE = DATA_DIR / "watsonx_logs.json"

# In-memory storage (loaded from persistent storage)
blogs_db = {}
comments_db = {}
watsonx_logs = []  # List to store API logs, ordered by timestamp

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

def load_watsonx_logs_from_file():
    """Load WatsonX API logs from persistent storage."""
    global watsonx_logs
    try:
        if WATSONX_LOGS_FILE.exists():
            with open(WATSONX_LOGS_FILE, 'r', encoding='utf-8') as f:
                data = json.load(f)
                watsonx_logs = []
                for log_data in data:
                    # Convert datetime strings back to datetime objects
                    if 'request_timestamp' in log_data:
                        log_data['request_timestamp'] = datetime.fromisoformat(log_data['request_timestamp'].replace('Z', '+00:00'))
                    if 'response_timestamp' in log_data and log_data['response_timestamp']:
                        log_data['response_timestamp'] = datetime.fromisoformat(log_data['response_timestamp'].replace('Z', '+00:00'))
                    watsonx_logs.append(WatsonxAPILog(**log_data))
                # Sort by timestamp (newest first)
                watsonx_logs.sort(key=lambda x: x.request_timestamp, reverse=True)
                # Keep only last 200 logs
                watsonx_logs = watsonx_logs[:200]
                print(f"Loaded {len(watsonx_logs)} WatsonX API logs from persistent storage")
    except Exception as e:
        print(f"Error loading WatsonX logs from file: {e}")
        watsonx_logs = []

def save_watsonx_logs_to_file():
    """Save WatsonX API logs to persistent storage."""
    try:
        ensure_data_directory()
        # Keep only last 200 logs
        logs_to_save = watsonx_logs[:200]
        # Convert to serializable dict
        data = [log.model_dump(mode='json') for log in logs_to_save]
        
        with open(WATSONX_LOGS_FILE, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
    except Exception as e:
        print(f"Error saving WatsonX logs to file: {e}")

def log_watsonx_request(blog_id: str, prompt: str, model_used: str = "ibm/granite-4-h-small"):
    """Log a WatsonX API request."""
    global watsonx_logs
    log_entry = WatsonxAPILog(
        id=generate_id(),
        request_timestamp=get_current_timestamp(),
        blog_id=blog_id,
        prompt=prompt,
        model_used=model_used,
        success=False  # Will be updated when response is received
    )
    watsonx_logs.insert(0, log_entry)  # Add to beginning (newest first)
    return log_entry.id

def log_watsonx_response(log_id: str, response_content: str = None, error_message: str = None, processing_time_ms: int = None):
    """Update a WatsonX API log with response information."""
    global watsonx_logs
    for log_entry in watsonx_logs:
        if log_entry.id == log_id:
            log_entry.response_timestamp = get_current_timestamp()
            log_entry.response_content = response_content
            log_entry.error_message = error_message
            log_entry.processing_time_ms = processing_time_ms
            log_entry.success = response_content is not None
            break
    
    # Keep only last 200 logs
    watsonx_logs = watsonx_logs[:200]
    save_watsonx_logs_to_file()


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

@app.get("/watsonx-logs", response_model=APIResponse)
async def get_watsonx_logs(page: int = 1, page_size: int = 10):
    """Get WatsonX API logs with pagination."""
    try:
        # Calculate pagination
        total_logs = len(watsonx_logs)
        start_idx = (page - 1) * page_size
        end_idx = start_idx + page_size
        
        # Get logs for current page
        page_logs = watsonx_logs[start_idx:end_idx]
        logs_data = [log.model_dump(mode='json') for log in page_logs]
        
        # Calculate pagination info
        total_pages = (total_logs + page_size - 1) // page_size
        
        return APIResponse(
            success=True,
            message="WatsonX logs retrieved successfully",
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
    """Get image generation logs (placeholder - no longer used)."""
    try:
        # Return empty logs as image generation is no longer active
        return APIResponse(
            success=True,
            message="Image generation logs (feature deprecated)",
            data={
                "logs": [],
                "pagination": {
                    "current_page": page,
                    "page_size": page_size,
                    "total_logs": 0,
                    "total_pages": 0,
                    "has_next": False,
                    "has_prev": False
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
            current_version=0,
            latest_content=""  # Initialize with empty string instead of None
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
    """Generate new blog content using IBM watsonx AI."""
    try:
        if blog_id not in blogs_db:
            raise HTTPException(status_code=404, detail="Blog not found")
        
        blog = blogs_db[blog_id]
        prompt = request_data.get("prompt", "")
        generation_type = request_data.get("generation_type", "text")  # Default to text only
        
        if not prompt:
            raise HTTPException(status_code=400, detail="Prompt is required")
            
        # Force text-only generation (images disabled)
        generation_type = "text"
        
        # Get IBM watsonx client
        client = await get_watsonx_client()
        if not client:
            raise HTTPException(status_code=500, detail="IBM watsonx client not initialized")
        
        final_content = ""
        images_generated = False
        text_generated = False
        log_id = ""
        start_time = get_current_timestamp()
        
        try:
            # Generate text content only (images disabled)
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
4. Focus purely on text content with excellent structure and flow
5. Create comprehensive, detailed content that stands on its own
6. Use markdown formatting for headers, lists, and emphasis

{f"Based on the current content above, " + prompt if blog.latest_content else prompt}"""
            
            # Log the request with the correct model from config
            from services.watsonx_service.config import granite_config
            log_id = log_watsonx_request(blog_id, enhanced_prompt, granite_config.model_id)
            
            # Generate content with IBM watsonx
            generated_content = client.generate(enhanced_prompt)
            
            if not generated_content:
                raise Exception("IBM watsonx returned empty response")
            
            text_generated = True
            
            # Calculate processing time and log response
            end_time = get_current_timestamp()
            processing_time_ms = int((end_time - start_time).total_seconds() * 1000)
            log_watsonx_response(log_id, generated_content, "", processing_time_ms)
            
            # Text-only generation (no images)
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
            
            # Success message for text-only generation
            message = "Blog content generated successfully"
            
            return APIResponse(
                success=True,
                message=message,
                data={
                    "version": version_number,
                    "content": final_content,
                    "file_path": version_file,
                    "generation_type": "text",
                    "text_generated": text_generated,
                    "images_generated": False
                }
            )
            
        except Exception as ai_error:
            if log_id:
                end_time = get_current_timestamp()
                processing_time_ms = int((end_time - start_time).total_seconds() * 1000)
                log_watsonx_response(log_id, "", str(ai_error), processing_time_ms)
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
