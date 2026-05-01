from fastapi import FastAPI, Request, Form, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import httpx
from pathlib import Path
import sys
from typing import Optional, List

# Add the project root to the Python path
project_root = Path(__file__).parent.parent.parent
sys.path.append(str(project_root))

from shared.config import settings

app = FastAPI(
    title="Blog Writer UI",
    description="Web interface for the blog writer application",
    version="1.0.0"
)

# Set up templates and static files
templates_dir = Path(__file__).parent / "templates"
static_dir = Path(__file__).parent / "static"

# Create directories if they don't exist
templates_dir.mkdir(exist_ok=True)
static_dir.mkdir(exist_ok=True)

templates = Jinja2Templates(directory=str(templates_dir))

# Mount static files
app.mount("/static", StaticFiles(directory=str(static_dir)), name="static")

# Mount generated images directory (create it if it doesn't exist)
images_dir = project_root / "generated_images"
images_dir.mkdir(exist_ok=True)
app.mount("/images", StaticFiles(directory=str(images_dir)), name="images")

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    """Home page showing all blogs."""
    try:
        # Fetch blogs from API Gateway
        async with httpx.AsyncClient() as client:
            response = await client.get(f"http://localhost:{settings.api_gateway_port}/api/blogs")
            if response.status_code == 200:
                blogs_data = response.json()
                blogs = blogs_data.get("data", []) if blogs_data.get("success") else []
            else:
                blogs = []
    except:
        blogs = []
    
    return templates.TemplateResponse("home.html", {
        "request": request,
        "blogs": blogs
    })

@app.get("/create", response_class=HTMLResponse)
async def create_blog_page(request: Request):
    """Blog creation page."""
    return templates.TemplateResponse("create.html", {"request": request})

@app.post("/create")
async def create_blog_submit(
    request: Request,
    title: str = Form(...),
    description: str = Form(""),
    tags: str = Form(""),
    publication_site: str = Form(""),
    initial_prompt: str = Form(...)
):
    """Handle blog creation form submission."""
    try:
        # Prepare blog data
        blog_data = {
            "title": title,
            "description": description if description else None,
            "tags": [tag.strip() for tag in tags.split(",") if tag.strip()],
            "publication_site": publication_site if publication_site else None,
            "initial_prompt": initial_prompt
        }
        
        # Create blog via API Gateway
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"http://localhost:{settings.api_gateway_port}/api/blogs",
                json=blog_data
            )
            
            if response.status_code == 200:
                return RedirectResponse(url="/", status_code=303)
            else:
                error_msg = "Failed to create blog"
                return templates.TemplateResponse("create.html", {
                    "request": request,
                    "error": error_msg
                })
    except Exception as e:
        return templates.TemplateResponse("create.html", {
            "request": request,
            "error": str(e)
        })

@app.get("/blog/{blog_id}", response_class=HTMLResponse)
async def view_blog(request: Request, blog_id: str):
    """View/edit a specific blog."""
    try:
        # Fetch blog details
        async with httpx.AsyncClient() as client:
            blog_response = await client.get(
                f"http://localhost:{settings.api_gateway_port}/api/blogs/{blog_id}"
            )
            versions_response = await client.get(
                f"http://localhost:{settings.api_gateway_port}/api/blogs/{blog_id}/versions"
            )
            comments_response = await client.get(
                f"http://localhost:{settings.api_gateway_port}/api/blogs/{blog_id}/comments"
            )
            
            blog = None
            versions = []
            comments = []
            
            if blog_response.status_code == 200:
                blog_data = blog_response.json()
                blog = blog_data.get("data") if blog_data.get("success") else None
            
            if versions_response.status_code == 200:
                versions_data = versions_response.json()
                versions = versions_data.get("data", []) if versions_data.get("success") else []
            
            if comments_response.status_code == 200:
                comments_data = comments_response.json()
                comments = comments_data.get("data", []) if comments_data.get("success") else []
            
            if not blog:
                raise HTTPException(status_code=404, detail="Blog not found")
            
            return templates.TemplateResponse("blog_detail.html", {
                "request": request,
                "blog": blog,
                "versions": versions,
                "comments": comments
            })
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/blog/{blog_id}/generate")
async def generate_content(
    request: Request,
    blog_id: str,
    prompt: str = Form(...),
    generation_type: str = Form("all")  # Default to "all" for backward compatibility
):
    """Generate new content for a blog."""
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"http://localhost:{settings.api_gateway_port}/api/blogs/{blog_id}/generate",
                json={"prompt": prompt, "generation_type": generation_type}
            )
            
            if response.status_code == 200:
                return RedirectResponse(url=f"/blog/{blog_id}", status_code=303)
            else:
                # Try to get detailed error from response
                try:
                    error_data = response.json()
                    error_msg = error_data.get("detail", "Failed to generate content")
                except:
                    error_msg = f"Failed to generate content (HTTP {response.status_code})"
                return RedirectResponse(url=f"/blog/{blog_id}?error={error_msg}", status_code=303)
    except Exception as e:
        return RedirectResponse(url=f"/blog/{blog_id}?error={str(e)}", status_code=303)

@app.post("/blog/{blog_id}/comment")
async def add_comment(
    request: Request,
    blog_id: str,
    content: str = Form(...),
    requested_changes: str = Form("")
):
    """Add a comment to a blog."""
    try:
        comment_data = {
            "content": content,
            "requested_changes": requested_changes if requested_changes else None
        }
        
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"http://localhost:{settings.api_gateway_port}/api/blogs/{blog_id}/comments",
                json=comment_data
            )
            
            return RedirectResponse(url=f"/blog/{blog_id}", status_code=303)
    except Exception as e:
        return RedirectResponse(url=f"/blog/{blog_id}?error={str(e)}", status_code=303)

@app.get("/api/blogs/{blog_id}/versions/{version_num}/content")
async def get_blog_version_content(blog_id: str, version_num: int):
    """Proxy request to get blog version content."""
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"http://localhost:{settings.api_gateway_port}/api/blogs/{blog_id}/versions/{version_num}/content"
            )
            
            if response.status_code == 200:
                return response.json()
            else:
                return {"success": False, "message": "Failed to load content"}
    except Exception as e:
        return {"success": False, "message": f"Error: {str(e)}"}

@app.put("/api/blogs/{blog_id}/content")
async def update_blog_content(blog_id: str, content_data: dict):
    """Proxy request to update blog content."""
    try:
        async with httpx.AsyncClient() as client:
            response = await client.put(
                f"http://localhost:{settings.api_gateway_port}/api/blogs/{blog_id}/content",
                json=content_data
            )
            
            if response.status_code == 200:
                return response.json()
            else:
                return {"success": False, "message": "Failed to update content"}
    except Exception as e:
        return {"success": False, "message": f"Error: {str(e)}"}

@app.post("/blog/{blog_id}/content")
async def save_blog_content(
    request: Request,
    blog_id: str,
    content: str = Form(...)
):
    """Save manually edited blog content."""
    try:
        async with httpx.AsyncClient() as client:
            response = await client.put(
                f"http://localhost:{settings.api_gateway_port}/api/blogs/{blog_id}/content",
                json={"content": content}
            )
            
            if response.status_code == 200:
                return RedirectResponse(url=f"/blog/{blog_id}?success=Content saved successfully", status_code=303)
            else:
                error_msg = "Failed to save content"
                return RedirectResponse(url=f"/blog/{blog_id}?error={error_msg}", status_code=303)
    except Exception as e:
        return RedirectResponse(url=f"/blog/{blog_id}?error={str(e)}", status_code=303)

@app.post("/blog/{blog_id}/versions/{version_num}/delete")
async def delete_blog_version(
    request: Request,
    blog_id: str,
    version_num: int
):
    """Delete a specific blog version."""
    try:
        async with httpx.AsyncClient() as client:
            response = await client.delete(
                f"http://localhost:{settings.api_gateway_port}/api/blogs/{blog_id}/versions/{version_num}"
            )
            
            if response.status_code == 200:
                return RedirectResponse(url=f"/blog/{blog_id}?success=Version {version_num} deleted successfully", status_code=303)
            else:
                data = response.json() if response.headers.get("content-type", "").startswith("application/json") else {}
                error_msg = data.get("detail", "Failed to delete version")
                return RedirectResponse(url=f"/blog/{blog_id}?error={error_msg}", status_code=303)
    except Exception as e:
        return RedirectResponse(url=f"/blog/{blog_id}?error={str(e)}", status_code=303)

@app.get("/settings", response_class=HTMLResponse)
async def settings_page(request: Request):
    """Settings page."""
    try:
        # Fetch current settings
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"http://localhost:{settings.settings_service_port}/settings"
            )
            
            current_settings = {}
            if response.status_code == 200:
                settings_data = response.json()
                current_settings = settings_data.get("data", {}) if settings_data.get("success") else {}
            
            return templates.TemplateResponse("settings.html", {
                "request": request,
                "settings": current_settings
            })
    except Exception as e:
        return templates.TemplateResponse("settings.html", {
            "request": request,
            "error": str(e),
            "settings": {}
        })

@app.post("/settings")
async def update_settings(
    request: Request,
    gemini_api_key: str = Form(""),
    source_folder: str = Form(""),
    default_publication_site: str = Form(""),
    google_cloud_project: str = Form(""),
    google_cloud_location: str = Form("us-central1"),
    google_cloud_credentials_path: str = Form(""),
    imagen_enabled: bool = Form(False),
    imagen_model: str = Form("imagen-3")
):
    """Update settings."""
    try:
        settings_data = {}
        
        if gemini_api_key:
            settings_data["gemini_api_key"] = gemini_api_key
        if source_folder:
            settings_data["source_folder"] = source_folder
        if default_publication_site:
            settings_data["default_publication_site"] = default_publication_site
        
        # Handle Google Cloud Imagen settings
        if google_cloud_project:
            settings_data["google_cloud_project"] = google_cloud_project
        if google_cloud_location:
            settings_data["google_cloud_location"] = google_cloud_location
        if google_cloud_credentials_path:
            settings_data["google_cloud_credentials_path"] = google_cloud_credentials_path
        
        # Always include boolean and string fields (even if default values)
        settings_data["imagen_enabled"] = imagen_enabled
        settings_data["imagen_model"] = imagen_model
        
        async with httpx.AsyncClient() as client:
            response = await client.put(
                f"http://localhost:{settings.settings_service_port}/settings",
                json=settings_data
            )
            
            if response.status_code == 200:
                return RedirectResponse(url="/settings?success=1", status_code=303)
            else:
                return RedirectResponse(url="/settings?error=Failed to update settings", status_code=303)
    except Exception as e:
        return RedirectResponse(url=f"/settings?error={str(e)}", status_code=303)

@app.get("/gemini-logs", response_class=HTMLResponse)
async def gemini_logs_page(request: Request, page: int = 1):
    """Gemini API logs page with pagination."""
    try:
        # Fetch Gemini logs from blog service
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"http://localhost:{settings.blog_service_port}/gemini-logs?page={page}&page_size=10"
            )
            
            logs_data = []
            pagination = {}
            
            if response.status_code == 200:
                data = response.json()
                if data.get("success"):
                    logs_data = data.get("data", {}).get("logs", [])
                    pagination = data.get("data", {}).get("pagination", {})
            
            return templates.TemplateResponse("gemini_logs.html", {
                "request": request,
                "logs": logs_data,
                "pagination": pagination
            })
    except Exception as e:
        return templates.TemplateResponse("gemini_logs.html", {
            "request": request,
            "error": str(e),
            "logs": [],
            "pagination": {}
        })

@app.get("/imagen-logs", response_class=HTMLResponse)
async def imagen_logs_page(request: Request, page: int = 1):
    """Imagen API logs page with pagination."""
    try:
        # Fetch Imagen logs from blog service
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"http://localhost:{settings.blog_service_port}/imagen-logs?page={page}&page_size=10"
            )
            
            logs_data = []
            pagination = {}
            
            if response.status_code == 200:
                data = response.json()
                if data.get("success"):
                    logs_data = data.get("data", {}).get("logs", [])
                    pagination = data.get("data", {}).get("pagination", {})
            
            return templates.TemplateResponse("imagen_logs.html", {
                "request": request,
                "logs": logs_data,
                "pagination": pagination
            })
    except Exception as e:
        return templates.TemplateResponse("imagen_logs.html", {
            "request": request,
            "error": str(e),
            "logs": [],
            "pagination": {}
        })

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=settings.ui_service_port)
