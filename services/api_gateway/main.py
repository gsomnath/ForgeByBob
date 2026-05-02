from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
import httpx
from typing import Any, Dict
import os
from pathlib import Path
import sys

# Add the project root to the Python path
project_root = Path(__file__).parent.parent.parent
sys.path.append(str(project_root))

from shared.config import settings
from shared.models import APIResponse

app = FastAPI(
    title="Blog Writer API Gateway",
    description="Central API gateway for the blog writer microservice application",
    version="1.0.0"
)

# CORS middleware for frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# HTTP client for inter-service communication
async def get_http_client():
    async with httpx.AsyncClient() as client:
        yield client

@app.get("/")
async def root():
    """Root endpoint."""
    return APIResponse(
        success=True,
        message="Blog Writer API Gateway is running",
        data={"version": "1.0.0"}
    )

@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "service": "api-gateway"}

# Blog Service Endpoints
@app.get("/api/blogs")
async def get_blogs(client: httpx.AsyncClient = Depends(get_http_client)):
    """Get all blogs."""
    try:
        response = await client.get(f"{settings.blog_service_url}/blogs")
        response.raise_for_status()
        return response.json()
    except httpx.RequestError:
        raise HTTPException(status_code=503, detail="Blog service unavailable")
    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=e.response.status_code, detail=e.response.text)

@app.post("/api/blogs")
async def create_blog(blog_data: Dict[str, Any], client: httpx.AsyncClient = Depends(get_http_client)):
    """Create a new blog."""
    try:
        response = await client.post(f"{settings.blog_service_url}/blogs", json=blog_data)
        response.raise_for_status()
        return response.json()
    except httpx.RequestError:
        raise HTTPException(status_code=503, detail="Blog service unavailable")
    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=e.response.status_code, detail=e.response.text)

@app.get("/api/blogs/{blog_id}")
async def get_blog(blog_id: str, client: httpx.AsyncClient = Depends(get_http_client)):
    """Get a specific blog."""
    try:
        response = await client.get(f"{settings.blog_service_url}/blogs/{blog_id}")
        response.raise_for_status()
        return response.json()
    except httpx.RequestError:
        raise HTTPException(status_code=503, detail="Blog service unavailable")
    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=e.response.status_code, detail=e.response.text)

@app.put("/api/blogs/{blog_id}")
async def update_blog(blog_id: str, blog_data: Dict[str, Any], client: httpx.AsyncClient = Depends(get_http_client)):
    """Update a blog."""
    try:
        response = await client.put(f"{settings.blog_service_url}/blogs/{blog_id}", json=blog_data)
        response.raise_for_status()
        return response.json()
    except httpx.RequestError:
        raise HTTPException(status_code=503, detail="Blog service unavailable")
    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=e.response.status_code, detail=e.response.text)

@app.delete("/api/blogs/{blog_id}")
async def delete_blog(blog_id: str, client: httpx.AsyncClient = Depends(get_http_client)):
    """Delete a blog."""
    try:
        response = await client.delete(f"{settings.blog_service_url}/blogs/{blog_id}")
        response.raise_for_status()
        return response.json()
    except httpx.RequestError:
        raise HTTPException(status_code=503, detail="Blog service unavailable")
    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=e.response.status_code, detail=e.response.text)

@app.get("/api/blogs/{blog_id}/versions")
async def get_blog_versions(blog_id: str, client: httpx.AsyncClient = Depends(get_http_client)):
    """Get all versions of a blog."""
    try:
        response = await client.get(f"{settings.blog_service_url}/blogs/{blog_id}/versions")
        response.raise_for_status()
        return response.json()
    except httpx.RequestError:
        raise HTTPException(status_code=503, detail="Blog service unavailable")
    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=e.response.status_code, detail=e.response.text)

@app.get("/api/blogs/{blog_id}/versions/{version_num}/content")
async def get_blog_version_content(blog_id: str, version_num: int, client: httpx.AsyncClient = Depends(get_http_client)):
    """Get the content of a specific blog version."""
    try:
        response = await client.get(f"{settings.blog_service_url}/blogs/{blog_id}/versions/{version_num}/content")
        response.raise_for_status()
        return response.json()
    except httpx.RequestError:
        raise HTTPException(status_code=503, detail="Blog service unavailable")
    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=e.response.status_code, detail=e.response.text)

@app.put("/api/blogs/{blog_id}/content")
async def update_blog_content(blog_id: str, content_data: Dict[str, Any], client: httpx.AsyncClient = Depends(get_http_client)):
    """Update blog content manually."""
    try:
        response = await client.put(f"{settings.blog_service_url}/blogs/{blog_id}/content", json=content_data)
        response.raise_for_status()
        return response.json()
    except httpx.RequestError:
        raise HTTPException(status_code=503, detail="Blog service unavailable")
    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=e.response.status_code, detail=e.response.text)

@app.delete("/api/blogs/{blog_id}/versions/{version_num}")
async def delete_blog_version(blog_id: str, version_num: int, client: httpx.AsyncClient = Depends(get_http_client)):
    """Delete a specific blog version."""
    try:
        response = await client.delete(f"{settings.blog_service_url}/blogs/{blog_id}/versions/{version_num}")
        response.raise_for_status()
        return response.json()
    except httpx.RequestError:
        raise HTTPException(status_code=503, detail="Blog service unavailable")
    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=e.response.status_code, detail=e.response.text)

@app.post("/api/blogs/{blog_id}/generate")
async def generate_blog_content(blog_id: str, request_data: Dict[str, Any], client: httpx.AsyncClient = Depends(get_http_client)):
    """Generate new blog content using AI."""
    try:
        response = await client.post(f"{settings.blog_service_url}/blogs/{blog_id}/generate", json=request_data)
        response.raise_for_status()
        return response.json()
    except httpx.RequestError:
        raise HTTPException(status_code=503, detail="Blog service unavailable")
    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=e.response.status_code, detail=e.response.text)

@app.post("/api/blogs/{blog_id}/comments")
async def add_comment(blog_id: str, comment_data: Dict[str, Any], client: httpx.AsyncClient = Depends(get_http_client)):
    """Add a comment to a blog."""
    try:
        response = await client.post(f"{settings.blog_service_url}/blogs/{blog_id}/comments", json=comment_data)
        response.raise_for_status()
        return response.json()
    except httpx.RequestError:
        raise HTTPException(status_code=503, detail="Blog service unavailable")
    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=e.response.status_code, detail=e.response.text)

@app.get("/api/blogs/{blog_id}/comments")
async def get_blog_comments(blog_id: str, client: httpx.AsyncClient = Depends(get_http_client)):
    """Get all comments for a blog."""
    try:
        response = await client.get(f"{settings.blog_service_url}/blogs/{blog_id}/comments")
        response.raise_for_status()
        return response.json()
    except httpx.RequestError:
        raise HTTPException(status_code=503, detail="Blog service unavailable")
    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=e.response.status_code, detail=e.response.text)

# Logging Endpoints
@app.get("/api/watsonx-logs")
async def get_watsonx_logs(page: int = 1, page_size: int = 10, client: httpx.AsyncClient = Depends(get_http_client)):
    """Get WatsonX API logs."""
    try:
        response = await client.get(f"{settings.blog_service_url}/watsonx-logs?page={page}&page_size={page_size}")
        response.raise_for_status()
        return response.json()
    except httpx.RequestError:
        raise HTTPException(status_code=503, detail="Blog service unavailable")
    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=e.response.status_code, detail=e.response.text)

@app.get("/api/imagen-logs")
async def get_imagen_logs(page: int = 1, page_size: int = 10, client: httpx.AsyncClient = Depends(get_http_client)):
    """Get image generation logs (deprecated feature)."""
    try:
        response = await client.get(f"{settings.blog_service_url}/imagen-logs?page={page}&page_size={page_size}")
        response.raise_for_status()
        return response.json()
    except httpx.RequestError:
        raise HTTPException(status_code=503, detail="Blog service unavailable")
    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=e.response.status_code, detail=e.response.text)

# Settings Service Endpoints
@app.get("/api/settings")
async def get_settings(client: httpx.AsyncClient = Depends(get_http_client)):
    """Get application settings."""
    try:
        response = await client.get(f"{settings.settings_service_url}/settings")
        response.raise_for_status()
        return response.json()
    except httpx.RequestError:
        raise HTTPException(status_code=503, detail="Settings service unavailable")
    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=e.response.status_code, detail=e.response.text)

@app.put("/api/settings")
async def update_settings(settings_data: Dict[str, Any], client: httpx.AsyncClient = Depends(get_http_client)):
    """Update application settings."""
    try:
        response = await client.put(f"{settings.settings_service_url}/settings", json=settings_data)
        response.raise_for_status()
        return response.json()
    except httpx.RequestError:
        raise HTTPException(status_code=503, detail="Settings service unavailable")
    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=e.response.status_code, detail=e.response.text)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=settings.api_gateway_port)
