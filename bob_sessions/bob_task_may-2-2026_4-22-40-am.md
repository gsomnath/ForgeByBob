**User:**

<task>
getting error - ✓ Success!
{
  "success": false,
  "data": null,
  "error": "Failed to create blog: 422",
  "metadata": {},
  "timestamp": "2026-05-02T08:16:10.211906"
}
</task>
<environment_details>
# VSCode Visible Files
services\orchestration_service\agents\writer_agent.py

# VSCode Open Tabs
.vscode/settings.json,services/ui_service/templates/home.html,.bobalytics.json,.gitignore,services/orchestration_service/agent_base.py,services/orchestration_service/agents/publisher_agent.py,services/orchestration_service/agent_registry.py,services/orchestration_service/agents/writer_agent.py,stop_all_services.py,services/ui_service/main.py,services/orchestration_service/main.py,services/ui_service/templates/agent_dashboard.html,services/orchestration_service/pipeline_manager.py,test_agent_metadata.py,test_orchestration.py,enhancement1_B_delta_agent_dashboard.md,services/ui_service/templates/base.html,services/ui_service/templates/create.html,services/api_gateway/main.py,services/orchestration_service/agents/__init__.py

# Actively Running Terminals
## Terminal 1 (Active)
### Working Directory: `c:\workspace\ForgeByBob`
### Original command: `python start_all_services.py`
## Terminal 2 (Active)
### Working Directory: `c:\workspace\ForgeByBob`
### Original command: `python start_all_services.py`
## Terminal 3 (Active)
### Working Directory: `c:\workspace\ForgeByBob`
### Original command: `python start_all_services.py`
## Terminal 4 (Active)
### Working Directory: `c:\workspace\ForgeByBob`
### Original command: `python start_all_services.py`
## Terminal 5 (Active)
### Working Directory: `c:\workspace\ForgeByBob`
### Original command: `python start_all_services.py`
## Terminal 6 (Active)
### Working Directory: `c:\workspace\ForgeByBob`
### Original command: `python start_all_services.py`
## Terminal 7 (Active)
### Working Directory: `c:\workspace\ForgeByBob`
### Original command: `python stop_all_services.py; python start_all_services.py`
## Terminal 8 (Active)
### Working Directory: `c:\workspace\ForgeByBob`
### Original command: `python stop_all_services.py; Start-Sleep -Seconds 3; python start_all_services.py`
### New Output
INFO:     127.0.0.1:64842 - "GET /api/blogs HTTP/1.1" 200 OK
INFO:     127.0.0.1:60765 - "GET / HTTP/1.1" 200 OK
INFO:     127.0.0.1:60765 - "GET /.well-known/appspecific/com.chrome.devtools.json HTTP/1.1" 404 Not Found


# Current Time
Current time in ISO 8601 UTC format: 2026-05-02T08:16:59.439Z
User time zone: America/New_York, UTC-4:00

# Current Cost
$0.00

# Review Exclusions
The following file patterns are excluded from code reviews:
- .vscode/**

# Current Mode
<slug>code</slug>
<name>💻 Code</name>


# Current Workspace Directory (c:/workspace/ForgeByBob) Files
.bobalytics.json
.editorconfig
.env.example
.gitattributes
.gitignore
.pre-commit-config.yaml
Base_application_details.md
check_services.py
COMMIT_CHECKLIST.md
enhancement1_A_watsonx_foundation.md
enhancement1_agentic_orchestration.md
enhancement1_B_delta_agent_dashboard.md
enhancement1_B_watsonx_orchestrate_setup.md
enhancement1_C_research_agent.md
enhancement1_D_reviewer_agent_selfcorrection.md
enhancement1_E_realtime_dashboard.md
enhancement2_trust_governance.md
enhancement3_ibm_ace_integration.md
HACKATHON_SERVICES_SETUP.md
IBM_CREDENTIALS_SETUP_GUIDE.md
IMPLEMENTATION_GUIDE.md
ORCHESTRATION_IMPLEMENTATION_SUMMARY.md
pyproject.toml
README.md
requirements.txt
restart_services.bat
SECURITY.md
start_all_services.py
start_services.bat
stop_all_services.py
stop_services.bat
test_agent_metadata.py
test_orchestration.py
.github/
.vscode/
services/
services/api_gateway/
services/api_gateway/__init__.py
services/api_gateway/main.py
services/blog_service/
services/blog_service/__init__.py
services/blog_service/main.py
services/orchestration_service/
services/orchestration_service/__init__.py
services/orchestration_service/agent_base.py
services/orchestration_service/agent_registry.py
services/orchestration_service/main.py
services/orchestration_service/pipeline_manager.py
services/orchestration_service/README.md
services/orchestration_service/agents/
services/orchestration_service/agents/__init__.py
services/orchestration_service/agents/publisher_agent.py
services/orchestration_service/agents/writer_agent.py
services/settings_service/
services/settings_service/__init__.py
services/settings_service/main.py
services/ui_service/
services/ui_service/__init__.py
services/ui_service/main.py
services/ui_service/static/
services/ui_service/templates/
services/ui_service/templates/agent_dashboard.html
services/ui_service/templates/base.html
services/ui_service/templates/blog_detail.html
services/ui_service/templates/create.html
services/ui_service/templates/home.html
services/ui_service/templates/imagen_logs.html
services/ui_service/templates/settings.html
services/ui_service/templates/watsonx_logs.html
services/watsonx_service/
services/watsonx_service/__init__.py
services/watsonx_service/config.py
services/watsonx_service/granite_client.py
services/watsonx_service/main.py
services/watsonx_service/test_granite.py
shared/
shared/__init__.py
shared/config.py
shared/models.py
shared/utils.py
tests/
tests/conftest.py
tests/test_utils.py
You have not created a todo list yet. Create one with `update_todo_list` if your task is complicated or involves multiple steps.
</environment_details>

---

**Assistant:**

I'll help you debug this 422 error. Let me start by examining the relevant files to understand the blog creation flow.

<read_file>
<args>
<file>
<path>services/api_gateway/main.py</path>
</file>
<file>
<path>services/blog_service/main.py</path>
</file>
<file>
<path>services/ui_service/main.py</path>
</file>
<file>
<path>shared/models.py</path>
</file>
</args>
</read_file>

---

**User:**

[read_file for 4 files] Result:
<files>
<file><path>services/api_gateway/main.py</path>
<content lines="1-296">
  1 | from fastapi import FastAPI, HTTPException, Depends
  2 | from fastapi.middleware.cors import CORSMiddleware
  3 | import httpx
  4 | from typing import Any, Dict
  5 | import os
  6 | from pathlib import Path
  7 | import sys
  8 | 
  9 | # Add the project root to the Python path
 10 | project_root = Path(__file__).parent.parent.parent
 11 | sys.path.append(str(project_root))
 12 | 
 13 | from shared.config import settings
 14 | from shared.models import APIResponse
 15 | 
 16 | # Service URLs
 17 | ORCHESTRATION_SERVICE_URL = "http://localhost:8004"
 18 | 
 19 | app = FastAPI(
 20 |     title="Blog Writer API Gateway",
 21 |     description="Central API gateway for the blog writer microservice application",
 22 |     version="1.0.0"
 23 | )
 24 | 
 25 | # CORS middleware for frontend access
 26 | app.add_middleware(
 27 |     CORSMiddleware,
 28 |     allow_origins=["*"],  # Configure appropriately for production
 29 |     allow_credentials=True,
 30 |     allow_methods=["*"],
 31 |     allow_headers=["*"],
 32 | )
 33 | 
 34 | # HTTP client for inter-service communication
 35 | async def get_http_client():
 36 |     async with httpx.AsyncClient() as client:
 37 |         yield client
 38 | 
 39 | @app.get("/")
 40 | async def root():
 41 |     """Root endpoint."""
 42 |     return APIResponse(
 43 |         success=True,
 44 |         message="Blog Writer API Gateway is running",
 45 |         data={"version": "1.0.0"}
 46 |     )
 47 | 
 48 | @app.get("/health")
 49 | async def health_check():
 50 |     """Health check endpoint."""
 51 |     return {"status": "healthy", "service": "api-gateway"}
 52 | 
 53 | # Blog Service Endpoints
 54 | @app.get("/api/blogs")
 55 | async def get_blogs(client: httpx.AsyncClient = Depends(get_http_client)):
 56 |     """Get all blogs."""
 57 |     try:
 58 |         response = await client.get(f"{settings.blog_service_url}/blogs")
 59 |         response.raise_for_status()
 60 |         return response.json()
 61 |     except httpx.RequestError:
 62 |         raise HTTPException(status_code=503, detail="Blog service unavailable")
 63 |     except httpx.HTTPStatusError as e:
 64 |         raise HTTPException(status_code=e.response.status_code, detail=e.response.text)
 65 | 
 66 | @app.post("/api/blogs")
 67 | async def create_blog(blog_data: Dict[str, Any], client: httpx.AsyncClient = Depends(get_http_client)):
 68 |     """Create a new blog."""
 69 |     try:
 70 |         response = await client.post(f"{settings.blog_service_url}/blogs", json=blog_data)
 71 |         response.raise_for_status()
 72 |         return response.json()
 73 |     except httpx.RequestError:
 74 |         raise HTTPException(status_code=503, detail="Blog service unavailable")
 75 |     except httpx.HTTPStatusError as e:
 76 |         raise HTTPException(status_code=e.response.status_code, detail=e.response.text)
 77 | 
 78 | @app.get("/api/blogs/{blog_id}")
 79 | async def get_blog(blog_id: str, client: httpx.AsyncClient = Depends(get_http_client)):
 80 |     """Get a specific blog."""
 81 |     try:
 82 |         response = await client.get(f"{settings.blog_service_url}/blogs/{blog_id}")
 83 |         response.raise_for_status()
 84 |         return response.json()
 85 |     except httpx.RequestError:
 86 |         raise HTTPException(status_code=503, detail="Blog service unavailable")
 87 |     except httpx.HTTPStatusError as e:
 88 |         raise HTTPException(status_code=e.response.status_code, detail=e.response.text)
 89 | 
 90 | @app.put("/api/blogs/{blog_id}")
 91 | async def update_blog(blog_id: str, blog_data: Dict[str, Any], client: httpx.AsyncClient = Depends(get_http_client)):
 92 |     """Update a blog."""
 93 |     try:
 94 |         response = await client.put(f"{settings.blog_service_url}/blogs/{blog_id}", json=blog_data)
 95 |         response.raise_for_status()
 96 |         return response.json()
 97 |     except httpx.RequestError:
 98 |         raise HTTPException(status_code=503, detail="Blog service unavailable")
 99 |     except httpx.HTTPStatusError as e:
100 |         raise HTTPException(status_code=e.response.status_code, detail=e.response.text)
101 | 
102 | @app.delete("/api/blogs/{blog_id}")
103 | async def delete_blog(blog_id: str, client: httpx.AsyncClient = Depends(get_http_client)):
104 |     """Delete a blog."""
105 |     try:
106 |         response = await client.delete(f"{settings.blog_service_url}/blogs/{blog_id}")
107 |         response.raise_for_status()
108 |         return response.json()
109 |     except httpx.RequestError:
110 |         raise HTTPException(status_code=503, detail="Blog service unavailable")
111 |     except httpx.HTTPStatusError as e:
112 |         raise HTTPException(status_code=e.response.status_code, detail=e.response.text)
113 | 
114 | @app.get("/api/blogs/{blog_id}/versions")
115 | async def get_blog_versions(blog_id: str, client: httpx.AsyncClient = Depends(get_http_client)):
116 |     """Get all versions of a blog."""
117 |     try:
118 |         response = await client.get(f"{settings.blog_service_url}/blogs/{blog_id}/versions")
119 |         response.raise_for_status()
120 |         return response.json()
121 |     except httpx.RequestError:
122 |         raise HTTPException(status_code=503, detail="Blog service unavailable")
123 |     except httpx.HTTPStatusError as e:
124 |         raise HTTPException(status_code=e.response.status_code, detail=e.response.text)
125 | 
126 | @app.get("/api/blogs/{blog_id}/versions/{version_num}/content")
127 | async def get_blog_version_content(blog_id: str, version_num: int, client: httpx.AsyncClient = Depends(get_http_client)):
128 |     """Get the content of a specific blog version."""
129 |     try:
130 |         response = await client.get(f"{settings.blog_service_url}/blogs/{blog_id}/versions/{version_num}/content")
131 |         response.raise_for_status()
132 |         return response.json()
133 |     except httpx.RequestError:
134 |         raise HTTPException(status_code=503, detail="Blog service unavailable")
135 |     except httpx.HTTPStatusError as e:
136 |         raise HTTPException(status_code=e.response.status_code, detail=e.response.text)
137 | 
138 | @app.put("/api/blogs/{blog_id}/content")
139 | async def update_blog_content(blog_id: str, content_data: Dict[str, Any], client: httpx.AsyncClient = Depends(get_http_client)):
140 |     """Update blog content manually."""
141 |     try:
142 |         response = await client.put(f"{settings.blog_service_url}/blogs/{blog_id}/content", json=content_data)
143 |         response.raise_for_status()
144 |         return response.json()
145 |     except httpx.RequestError:
146 |         raise HTTPException(status_code=503, detail="Blog service unavailable")
147 |     except httpx.HTTPStatusError as e:
148 |         raise HTTPException(status_code=e.response.status_code, detail=e.response.text)
149 | 
150 | @app.delete("/api/blogs/{blog_id}/versions/{version_num}")
151 | async def delete_blog_version(blog_id: str, version_num: int, client: httpx.AsyncClient = Depends(get_http_client)):
152 |     """Delete a specific blog version."""
153 |     try:
154 |         response = await client.delete(f"{settings.blog_service_url}/blogs/{blog_id}/versions/{version_num}")
155 |         response.raise_for_status()
156 |         return response.json()
157 |     except httpx.RequestError:
158 |         raise HTTPException(status_code=503, detail="Blog service unavailable")
159 |     except httpx.HTTPStatusError as e:
160 |         raise HTTPException(status_code=e.response.status_code, detail=e.response.text)
161 | 
162 | @app.post("/api/blogs/{blog_id}/generate")
163 | async def generate_blog_content(blog_id: str, request_data: Dict[str, Any], client: httpx.AsyncClient = Depends(get_http_client)):
164 |     """Generate new blog content using AI."""
165 |     try:
166 |         response = await client.post(f"{settings.blog_service_url}/blogs/{blog_id}/generate", json=request_data)
167 |         response.raise_for_status()
168 |         return response.json()
169 |     except httpx.RequestError:
170 |         raise HTTPException(status_code=503, detail="Blog service unavailable")
171 |     except httpx.HTTPStatusError as e:
172 |         raise HTTPException(status_code=e.response.status_code, detail=e.response.text)
173 | 
174 | @app.post("/api/blogs/{blog_id}/comments")
175 | async def add_comment(blog_id: str, comment_data: Dict[str, Any], client: httpx.AsyncClient = Depends(get_http_client)):
176 |     """Add a comment to a blog."""
177 |     try:
178 |         response = await client.post(f"{settings.blog_service_url}/blogs/{blog_id}/comments", json=comment_data)
179 |         response.raise_for_status()
180 |         return response.json()
181 |     except httpx.RequestError:
182 |         raise HTTPException(status_code=503, detail="Blog service unavailable")
183 |     except httpx.HTTPStatusError as e:
184 |         raise HTTPException(status_code=e.response.status_code, detail=e.response.text)
185 | 
186 | @app.get("/api/blogs/{blog_id}/comments")
187 | async def get_blog_comments(blog_id: str, client: httpx.AsyncClient = Depends(get_http_client)):
188 |     """Get all comments for a blog."""
189 |     try:
190 |         response = await client.get(f"{settings.blog_service_url}/blogs/{blog_id}/comments")
191 |         response.raise_for_status()
192 |         return response.json()
193 |     except httpx.RequestError:
194 |         raise HTTPException(status_code=503, detail="Blog service unavailable")
195 |     except httpx.HTTPStatusError as e:
196 |         raise HTTPException(status_code=e.response.status_code, detail=e.response.text)
197 | 
198 | # Logging Endpoints
199 | @app.get("/api/watsonx-logs")
200 | async def get_watsonx_logs(page: int = 1, page_size: int = 10, client: httpx.AsyncClient = Depends(get_http_client)):
201 |     """Get WatsonX API logs."""
202 |     try:
203 |         response = await client.get(f"{settings.blog_service_url}/watsonx-logs?page={page}&page_size={page_size}")
204 |         response.raise_for_status()
205 |         return response.json()
206 |     except httpx.RequestError:
207 |         raise HTTPException(status_code=503, detail="Blog service unavailable")
208 |     except httpx.HTTPStatusError as e:
209 |         raise HTTPException(status_code=e.response.status_code, detail=e.response.text)
210 | 
211 | @app.get("/api/imagen-logs")
212 | async def get_imagen_logs(page: int = 1, page_size: int = 10, client: httpx.AsyncClient = Depends(get_http_client)):
213 |     """Get image generation logs (deprecated feature)."""
214 |     try:
215 |         response = await client.get(f"{settings.blog_service_url}/imagen-logs?page={page}&page_size={page_size}")
216 |         response.raise_for_status()
217 |         return response.json()
218 |     except httpx.RequestError:
219 |         raise HTTPException(status_code=503, detail="Blog service unavailable")
220 |     except httpx.HTTPStatusError as e:
221 |         raise HTTPException(status_code=e.response.status_code, detail=e.response.text)
222 | 
223 | # Settings Service Endpoints
224 | @app.get("/api/settings")
225 | async def get_settings(client: httpx.AsyncClient = Depends(get_http_client)):
226 |     """Get application settings."""
227 |     try:
228 |         response = await client.get(f"{settings.settings_service_url}/settings")
229 |         response.raise_for_status()
230 |         return response.json()
231 |     except httpx.RequestError:
232 |         raise HTTPException(status_code=503, detail="Settings service unavailable")
233 |     except httpx.HTTPStatusError as e:
234 |         raise HTTPException(status_code=e.response.status_code, detail=e.response.text)
235 | 
236 | @app.put("/api/settings")
237 | async def update_settings(settings_data: Dict[str, Any], client: httpx.AsyncClient = Depends(get_http_client)):
238 |     """Update application settings."""
239 |     try:
240 |         response = await client.put(f"{settings.settings_service_url}/settings", json=settings_data)
241 |         response.raise_for_status()
242 |         return response.json()
243 |     except httpx.RequestError:
244 |         raise HTTPException(status_code=503, detail="Settings service unavailable")
245 |     except httpx.HTTPStatusError as e:
246 |         raise HTTPException(status_code=e.response.status_code, detail=e.response.text)
247 | 
248 | # Orchestration Service Endpoints
249 | @app.post("/api/blogs/generate-orchestrated")
250 | async def generate_blog_orchestrated(request: dict):
251 |     """Generate blog using orchestration service"""
252 |     try:
253 |         async with httpx.AsyncClient() as client:
254 |             response = await client.post(
255 |                 f"{ORCHESTRATION_SERVICE_URL}/blog/generate",
256 |                 json=request,
257 |                 timeout=60.0
258 |             )
259 |             return response.json()
260 |     except Exception as e:
261 |         raise HTTPException(status_code=500, detail=str(e))
262 | 
263 | @app.get("/api/orchestration/pipelines")
264 | async def list_pipelines():
265 |     """List all orchestration pipelines"""
266 |     try:
267 |         async with httpx.AsyncClient() as client:
268 |             response = await client.get(f"{ORCHESTRATION_SERVICE_URL}/pipelines")
269 |             return response.json()
270 |     except Exception as e:
271 |         raise HTTPException(status_code=500, detail=str(e))
272 | 
273 | @app.get("/api/orchestration/agents")
274 | async def list_agents():
275 |     """List all registered agents"""
276 |     try:
277 |         async with httpx.AsyncClient() as client:
278 |             response = await client.get(f"{ORCHESTRATION_SERVICE_URL}/agents")
279 |             return response.json()
280 |     except Exception as e:
281 |         raise HTTPException(status_code=500, detail=str(e))
282 | 
283 | 
284 | @app.get("/api/orchestration/metrics")
285 | async def get_orchestration_metrics():
286 |     """Get orchestration metrics"""
287 |     try:
288 |         async with httpx.AsyncClient() as client:
289 |             response = await client.get(f"{ORCHESTRATION_SERVICE_URL}/metrics")
290 |             return response.json()
291 |     except Exception as e:
292 |         raise HTTPException(status_code=500, detail=str(e))
293 | 
294 | if __name__ == "__main__":
295 |     import uvicorn
296 |     uvicorn.run(app, host="0.0.0.0", port=settings.api_gateway_port)
</content>
</file>
<file><path>services/blog_service/main.py</path>
<content lines="1-885">
  1 | from fastapi import FastAPI, HTTPException, Depends
  2 | from contextlib import asynccontextmanager
  3 | import os
  4 | import httpx
  5 | from typing import List, Optional
  6 | from pathlib import Path
  7 | import sys
  8 | import json
  9 | import base64
 10 | import hashlib
 11 | import uuid
 12 | import asyncio
 13 | from datetime import datetime, timezone
 14 | 
 15 | # Add the project root to the Python path
 16 | project_root = Path(__file__).parent.parent.parent
 17 | sys.path.append(str(project_root))
 18 | 
 19 | from shared.config import settings
 20 | from shared.models import (
 21 |     Blog, BlogCreate, BlogUpdate, BlogVersion, Comment, CommentCreate,
 22 |     APIResponse, BlogStatus, WatsonxAPILog
 23 | )
 24 | from shared.utils import (
 25 |     generate_id, get_current_timestamp, create_blog_folder_structure, save_blog_version,
 26 |     save_prompt, get_next_version_number, list_blog_versions,
 27 |     read_file_content, ensure_directory_exists
 28 | )
 29 | 
 30 | # Import IBM watsonx client
 31 | from services.watsonx_service.granite_client import get_granite_client
 32 | 
 33 | # Image generation will use placeholder images
 34 | IMAGEN_AVAILABLE = False
 35 | 
 36 | @asynccontextmanager
 37 | async def lifespan(app: FastAPI):
 38 |     """Manage application lifecycle."""
 39 |     ensure_directory_exists(settings.source_folder)
 40 |     ensure_data_directory()
 41 |     load_blogs_from_file()
 42 |     load_comments_from_file()
 43 |     load_watsonx_logs_from_file()
 44 |     yield
 45 | 
 46 | 
 47 | app = FastAPI(
 48 |     title="Blog Service",
 49 |     description="Microservice for blog content management and AI generation",
 50 |     version="1.0.0",
 51 |     lifespan=lifespan
 52 | )
 53 | 
 54 | # IBM watsonx client (initialized globally)
 55 | watsonx_client = None
 56 | 
 57 | async def get_watsonx_client():
 58 |     """Get or initialize IBM watsonx client."""
 59 |     global watsonx_client
 60 |     if watsonx_client is None:
 61 |         watsonx_client = get_granite_client()
 62 |     return watsonx_client
 63 | 
 64 | async def get_current_settings():
 65 |     """Get all current settings from settings service."""
 66 |     try:
 67 |         async with httpx.AsyncClient() as client:
 68 |             response = await client.get(f"{settings.settings_service_url}/settings/raw", timeout=5.0)
 69 |             if response.status_code == 200:
 70 |                 data = response.json()
 71 |                 if data.get("success") and data.get("data"):
 72 |                     return data["data"]
 73 |     except Exception as e:
 74 |         print(f"Warning: Settings service exception: {e}")
 75 |     return None
 76 | 
 77 | 
 78 | async def generate_image_prompts_with_watsonx(content: str, blog_title: str, user_prompt: str = "") -> List[str]:
 79 |     """Use IBM watsonx.ai to generate high-quality image prompts based on blog content."""
 80 |     try:
 81 |         # Get watsonx client
 82 |         client = await get_watsonx_client()
 83 |         if not client:
 84 |             # Fallback to default prompts
 85 |             return [
 86 |                 f"Professional illustration related to {blog_title}, clean modern style, high quality, detailed artwork",
 87 |                 f"Abstract representation of {blog_title} concept, minimalist design, professional quality"
 88 |             ]
 89 |         
 90 |         # Include user prompt if provided
 91 |         user_prompt_context = ""
 92 |         if user_prompt:
 93 |             user_prompt_context = f"""
 94 | 
 95 | Additional User Requirements for Images: {user_prompt}
 96 | Please incorporate these requirements into the image prompts where relevant.
 97 | """
 98 |         
 99 |         # Create a prompt for watsonx to generate image descriptions
100 |         watsonx_prompt = f"""
101 | Based on this blog post title and content, create 2 detailed, high-quality image generation prompts that would create visually appealing images to accompany the article.
102 | 
103 | Blog Title: {blog_title}
104 | 
105 | Blog Content Excerpt: {content[:1000]}...{user_prompt_context}
106 | 
107 | Requirements for each image prompt:
108 | - Professional, high-quality visual style
109 | - Relevant to the blog content themes
110 | - Descriptive enough for AI image generation
111 | - Avoid text/words in images
112 | - Modern, clean aesthetic
113 | - Each prompt should be different and complementary
114 | 
115 | Please provide exactly 2 image prompts, each on a separate line, starting with "Image 1:" and "Image 2:"
116 | """
117 | 
118 |         # Generate prompts using IBM watsonx
119 |         response = client.generate(watsonx_prompt, max_tokens=500)
120 |         generated_text = response.strip()
121 |         
122 |         # Parse the generated prompts
123 |         image_prompts = []
124 |         lines = generated_text.split('\n')
125 |         
126 |         for line in lines:
127 |             line = line.strip()
128 |             if line.startswith("Image 1:"):
129 |                 image_prompts.append(line.replace("Image 1:", "").strip())
130 |             elif line.startswith("Image 2:"):
131 |                 image_prompts.append(line.replace("Image 2:", "").strip())
132 |         
133 |         # Ensure we have exactly 2 prompts
134 |         if len(image_prompts) < 2:
135 |             # Fallback if parsing failed
136 |             image_prompts = [
137 |                 f"Professional illustration related to {blog_title}, clean modern style, high quality, detailed artwork",
138 |                 f"Abstract representation of {blog_title} concept, minimalist design, professional quality"
139 |             ]
140 |         
141 |         return image_prompts[:2]  # Ensure exactly 2 prompts
142 |         
143 |     except Exception as e:
144 |         print(f"Error generating image prompts with IBM watsonx: {e}")
145 |         # Fallback to default prompts
146 |         return [
147 |             f"Professional illustration related to {blog_title}, clean modern style, high quality, detailed artwork",
148 |             f"Abstract representation of {blog_title} concept, minimalist design, professional quality"
149 |         ]
150 | 
151 | def generate_static_image_url(blog_id: str, image_number: int) -> str:
152 |     """Generate a static image URL that won't change on page refresh."""
153 |     seed = f"{blog_id}_{image_number}"
154 |     hash_value = hashlib.md5(seed.encode()).hexdigest()
155 |     image_id = int(hash_value[:6], 16) % 1000 + 1
156 |     return f"https://picsum.photos/id/{image_id}/800/600"
157 | 
158 | def save_imagen_response_to_file(imagen_response, blog_id: str, image_number: int) -> Optional[str]:
159 |     """Save Imagen API response image to local file and return the URL."""
160 |     try:
161 |         # Create images directory if it doesn't exist
162 |         images_dir = Path("generated_images")
163 |         images_dir.mkdir(exist_ok=True)
164 |         
165 |         # Create filename with blog_id and image number
166 |         filename = f"{blog_id}_image_{image_number}_{uuid.uuid4().hex[:8]}.png"
167 |         file_path = images_dir / filename
168 |         
169 |         # Get the first image from the response
170 |         if imagen_response.images and len(imagen_response.images) > 0:
171 |             image = imagen_response.images[0]
172 |             
173 |             # Save the image to file
174 |             with open(file_path, "wb") as f:
175 |                 f.write(image._image_bytes)
176 |             
177 |             # Return local URL that will be served by UI service
178 |             return f"http://localhost:8003/images/{filename}"
179 |         
180 |         return None
181 |     except Exception as e:
182 |         print(f"Error saving Imagen response to file: {e}")
183 |         return None
184 | 
185 | async def generate_images_with_placeholder(content: str, blog_title: str, blog_id: str, user_prompt: str = "") -> List[str]:
186 |     """Image generation is disabled. Returns empty list."""
187 |     # Image generation functionality has been disabled
188 |     return []
189 | 
190 | # Persistent storage paths
191 | DATA_DIR = Path("data")
192 | BLOGS_DB_FILE = DATA_DIR / "blogs.json"
193 | COMMENTS_DB_FILE = DATA_DIR / "comments.json"
194 | WATSONX_LOGS_FILE = DATA_DIR / "watsonx_logs.json"
195 | 
196 | # In-memory storage (loaded from persistent storage)
197 | blogs_db = {}
198 | comments_db = {}
199 | watsonx_logs = []  # List to store API logs, ordered by timestamp
200 | 
201 | def ensure_data_directory():
202 |     """Ensure data directory exists."""
203 |     DATA_DIR.mkdir(exist_ok=True)
204 | 
205 | def load_blogs_from_file():
206 |     """Load blogs from persistent storage."""
207 |     global blogs_db
208 |     try:
209 |         if BLOGS_DB_FILE.exists():
210 |             with open(BLOGS_DB_FILE, 'r', encoding='utf-8') as f:
211 |                 data = json.load(f)
212 |                 # Convert back to Blog objects
213 |                 for blog_id, blog_data in data.items():
214 |                     # Convert datetime strings back to datetime objects
215 |                     if 'created_at' in blog_data:
216 |                         blog_data['created_at'] = datetime.fromisoformat(blog_data['created_at'].replace('Z', '+00:00'))
217 |                     if 'updated_at' in blog_data:
218 |                         blog_data['updated_at'] = datetime.fromisoformat(blog_data['updated_at'].replace('Z', '+00:00'))
219 |                     blogs_db[blog_id] = Blog(**blog_data)
220 |                 print(f"Loaded {len(blogs_db)} blogs from persistent storage")
221 |     except Exception as e:
222 |         print(f"Error loading blogs from file: {e}")
223 |         blogs_db = {}
224 | 
225 | def save_blogs_to_file():
226 |     """Save blogs to persistent storage."""
227 |     try:
228 |         ensure_data_directory()
229 |         # Convert Blog objects to serializable dict
230 |         data = {}
231 |         for blog_id, blog in blogs_db.items():
232 |             blog_dict = blog.model_dump(mode='json')
233 |             data[blog_id] = blog_dict
234 |         
235 |         with open(BLOGS_DB_FILE, 'w', encoding='utf-8') as f:
236 |             json.dump(data, f, indent=2, ensure_ascii=False)
237 |     except Exception as e:
238 |         print(f"Error saving blogs to file: {e}")
239 | 
240 | def load_comments_from_file():
241 |     """Load comments from persistent storage."""
242 |     global comments_db
243 |     try:
244 |         if COMMENTS_DB_FILE.exists():
245 |             with open(COMMENTS_DB_FILE, 'r', encoding='utf-8') as f:
246 |                 data = json.load(f)
247 |                 # Convert back to Comment objects
248 |                 for blog_id, comments_list in data.items():
249 |                     comments_db[blog_id] = []
250 |                     for comment_data in comments_list:
251 |                         # Convert datetime strings back to datetime objects
252 |                         if 'created_at' in comment_data:
253 |                             comment_data['created_at'] = datetime.fromisoformat(comment_data['created_at'].replace('Z', '+00:00'))
254 |                         comments_db[blog_id].append(Comment(**comment_data))
255 |                 print(f"Loaded comments for {len(comments_db)} blogs from persistent storage")
256 |     except Exception as e:
257 |         print(f"Error loading comments from file: {e}")
258 |         comments_db = {}
259 | 
260 | def save_comments_to_file():
261 |     """Save comments to persistent storage."""
262 |     try:
263 |         ensure_data_directory()
264 |         # Convert Comment objects to serializable dict
265 |         data = {}
266 |         for blog_id, comments_list in comments_db.items():
267 |             data[blog_id] = [comment.model_dump(mode='json') for comment in comments_list]
268 |         
269 |         with open(COMMENTS_DB_FILE, 'w', encoding='utf-8') as f:
270 |             json.dump(data, f, indent=2, ensure_ascii=False)
271 |     except Exception as e:
272 |         print(f"Error saving comments to file: {e}")
273 | 
274 | def load_watsonx_logs_from_file():
275 |     """Load WatsonX API logs from persistent storage."""
276 |     global watsonx_logs
277 |     try:
278 |         if WATSONX_LOGS_FILE.exists():
279 |             with open(WATSONX_LOGS_FILE, 'r', encoding='utf-8') as f:
280 |                 data = json.load(f)
281 |                 watsonx_logs = []
282 |                 for log_data in data:
283 |                     # Convert datetime strings back to datetime objects
284 |                     if 'request_timestamp' in log_data:
285 |                         log_data['request_timestamp'] = datetime.fromisoformat(log_data['request_timestamp'].replace('Z', '+00:00'))
286 |                     if 'response_timestamp' in log_data and log_data['response_timestamp']:
287 |                         log_data['response_timestamp'] = datetime.fromisoformat(log_data['response_timestamp'].replace('Z', '+00:00'))
288 |                     watsonx_logs.append(WatsonxAPILog(**log_data))
289 |                 # Sort by timestamp (newest first)
290 |                 watsonx_logs.sort(key=lambda x: x.request_timestamp, reverse=True)
291 |                 # Keep only last 200 logs
292 |                 watsonx_logs = watsonx_logs[:200]
293 |                 print(f"Loaded {len(watsonx_logs)} WatsonX API logs from persistent storage")
294 |     except Exception as e:
295 |         print(f"Error loading WatsonX logs from file: {e}")
296 |         watsonx_logs = []
297 | 
298 | def save_watsonx_logs_to_file():
299 |     """Save WatsonX API logs to persistent storage."""
300 |     try:
301 |         ensure_data_directory()
302 |         # Keep only last 200 logs
303 |         logs_to_save = watsonx_logs[:200]
304 |         # Convert to serializable dict
305 |         data = [log.model_dump(mode='json') for log in logs_to_save]
306 |         
307 |         with open(WATSONX_LOGS_FILE, 'w', encoding='utf-8') as f:
308 |             json.dump(data, f, indent=2, ensure_ascii=False)
309 |     except Exception as e:
310 |         print(f"Error saving WatsonX logs to file: {e}")
311 | 
312 | def log_watsonx_request(blog_id: str, prompt: str, model_used: str = "ibm/granite-4-h-small"):
313 |     """Log a WatsonX API request."""
314 |     global watsonx_logs
315 |     log_entry = WatsonxAPILog(
316 |         id=generate_id(),
317 |         request_timestamp=get_current_timestamp(),
318 |         blog_id=blog_id,
319 |         prompt=prompt,
320 |         model_used=model_used,
321 |         success=False  # Will be updated when response is received
322 |     )
323 |     watsonx_logs.insert(0, log_entry)  # Add to beginning (newest first)
324 |     return log_entry.id
325 | 
326 | def log_watsonx_response(log_id: str, response_content: Optional[str] = None, error_message: Optional[str] = None, processing_time_ms: Optional[int] = None):
327 |     """Update a WatsonX API log with response information."""
328 |     global watsonx_logs
329 |     for log_entry in watsonx_logs:
330 |         if log_entry.id == log_id:
331 |             log_entry.response_timestamp = get_current_timestamp()
332 |             log_entry.response_content = response_content
333 |             log_entry.error_message = error_message
334 |             log_entry.processing_time_ms = processing_time_ms
335 |             log_entry.success = response_content is not None
336 |             break
337 |     
338 |     # Keep only last 200 logs
339 |     watsonx_logs = watsonx_logs[:200]
340 |     save_watsonx_logs_to_file()
341 | 
342 | 
343 | @app.get("/")
344 | async def root():
345 |     """Root endpoint."""
346 |     return APIResponse(
347 |         success=True,
348 |         message="Blog Service is running",
349 |         data={"version": "1.0.0"}
350 |     )
351 | 
352 | @app.get("/health")
353 | async def health_check():
354 |     """Health check endpoint."""
355 |     return {"status": "healthy", "service": "blog-service"}
356 | 
357 | @app.get("/watsonx-logs", response_model=APIResponse)
358 | async def get_watsonx_logs(page: int = 1, page_size: int = 10):
359 |     """Get WatsonX API logs with pagination."""
360 |     try:
361 |         # Calculate pagination
362 |         total_logs = len(watsonx_logs)
363 |         start_idx = (page - 1) * page_size
364 |         end_idx = start_idx + page_size
365 |         
366 |         # Get logs for current page
367 |         page_logs = watsonx_logs[start_idx:end_idx]
368 |         logs_data = [log.model_dump(mode='json') for log in page_logs]
369 |         
370 |         # Calculate pagination info
371 |         total_pages = (total_logs + page_size - 1) // page_size
372 |         
373 |         return APIResponse(
374 |             success=True,
375 |             message="WatsonX logs retrieved successfully",
376 |             data={
377 |                 "logs": logs_data,
378 |                 "pagination": {
379 |                     "current_page": page,
380 |                     "page_size": page_size,
381 |                     "total_logs": total_logs,
382 |                     "total_pages": total_pages,
383 |                     "has_next": page < total_pages,
384 |                     "has_prev": page > 1
385 |                 }
386 |             }
387 |         )
388 |     except Exception as e:
389 |         raise HTTPException(status_code=500, detail=str(e))
390 | 
391 | @app.get("/imagen-logs", response_model=APIResponse)
392 | async def get_imagen_logs(page: int = 1, page_size: int = 10):
393 |     """Get image generation logs (placeholder - no longer used)."""
394 |     try:
395 |         # Return empty logs as image generation is no longer active
396 |         return APIResponse(
397 |             success=True,
398 |             message="Image generation logs (feature deprecated)",
399 |             data={
400 |                 "logs": [],
401 |                 "pagination": {
402 |                     "current_page": page,
403 |                     "page_size": page_size,
404 |                     "total_logs": 0,
405 |                     "total_pages": 0,
406 |                     "has_next": False,
407 |                     "has_prev": False
408 |                 }
409 |             }
410 |         )
411 |     except Exception as e:
412 |         raise HTTPException(status_code=500, detail=str(e))
413 |         
414 | 
415 | @app.post("/blogs", response_model=APIResponse)
416 | async def create_blog(blog_data: BlogCreate):
417 |     """Create a new blog."""
418 |     try:
419 |         blog_id = generate_id()
420 |         
421 |         # Create folder structure
422 |         folder_path = create_blog_folder_structure(settings.source_folder, blog_data.title)
423 |         
424 |         # Save initial prompt
425 |         save_prompt(folder_path, blog_data.initial_prompt, "initial_prompt.txt")
426 |         
427 |         # Create blog record
428 |         blog = Blog(
429 |             id=blog_id,
430 |             title=blog_data.title,
431 |             description=blog_data.description,
432 |             tags=blog_data.tags,
433 |             publication_site=blog_data.publication_site,
434 |             status=BlogStatus.DRAFT,
435 |             created_at=get_current_timestamp(),
436 |             updated_at=get_current_timestamp(),
437 |             folder_path=folder_path,
438 |             current_version=0,
439 |             latest_content=""  # Initialize with empty string instead of None
440 |         )
441 |         
442 |         blogs_db[blog_id] = blog
443 |         save_blogs_to_file()  # Save to persistent storage
444 |         
445 |         return APIResponse(
446 |             success=True,
447 |             message="Blog created successfully",
448 |             data=blog.model_dump(mode='json')
449 |         )
450 |     except Exception as e:
451 |         raise HTTPException(status_code=500, detail=str(e))
452 | 
453 | @app.get("/blogs", response_model=APIResponse)
454 | async def get_blogs():
455 |     """Get all blogs."""
456 |     try:
457 |         blogs_list = [blog.model_dump(mode='json') for blog in blogs_db.values()]
458 |         return APIResponse(
459 |             success=True,
460 |             message="Blogs retrieved successfully",
461 |             data=blogs_list
462 |         )
463 |     except Exception as e:
464 |         raise HTTPException(status_code=500, detail=str(e))
465 | 
466 | @app.get("/blogs/{blog_id}", response_model=APIResponse)
467 | async def get_blog(blog_id: str):
468 |     """Get a specific blog."""
469 |     try:
470 |         if blog_id not in blogs_db:
471 |             raise HTTPException(status_code=404, detail="Blog not found")
472 |         
473 |         blog = blogs_db[blog_id]
474 |         return APIResponse(
475 |             success=True,
476 |             message="Blog retrieved successfully",
477 |             data=blog.model_dump(mode='json')
478 |         )
479 |     except HTTPException:
480 |         raise
481 |     except Exception as e:
482 |         raise HTTPException(status_code=500, detail=str(e))
483 | 
484 | @app.put("/blogs/{blog_id}", response_model=APIResponse)
485 | async def update_blog(blog_id: str, blog_update: BlogUpdate):
486 |     """Update a blog."""
487 |     try:
488 |         if blog_id not in blogs_db:
489 |             raise HTTPException(status_code=404, detail="Blog not found")
490 |         
491 |         blog = blogs_db[blog_id]
492 |         
493 |         # Update fields
494 |         if blog_update.title is not None:
495 |             blog.title = blog_update.title
496 |         if blog_update.description is not None:
497 |             blog.description = blog_update.description
498 |         if blog_update.tags is not None:
499 |             blog.tags = blog_update.tags
500 |         if blog_update.publication_site is not None:
501 |             blog.publication_site = blog_update.publication_site
502 |         if blog_update.status is not None:
503 |             blog.status = blog_update.status
504 |         
505 |         blog.updated_at = get_current_timestamp()
506 |         save_blogs_to_file()  # Save to persistent storage
507 |         
508 |         return APIResponse(
509 |             success=True,
510 |             message="Blog updated successfully",
511 |             data=blog.model_dump(mode='json')
512 |         )
513 |     except HTTPException:
514 |         raise
515 |     except Exception as e:
516 |         raise HTTPException(status_code=500, detail=str(e))
517 | 
518 | @app.delete("/blogs/{blog_id}", response_model=APIResponse)
519 | async def delete_blog(blog_id: str):
520 |     """Delete a blog."""
521 |     try:
522 |         if blog_id not in blogs_db:
523 |             raise HTTPException(status_code=404, detail="Blog not found")
524 |         
525 |         del blogs_db[blog_id]
526 |         save_blogs_to_file()  # Save to persistent storage
527 |         
528 |         return APIResponse(
529 |             success=True,
530 |             message="Blog deleted successfully"
531 |         )
532 |     except HTTPException:
533 |         raise
534 |     except Exception as e:
535 |         raise HTTPException(status_code=500, detail=str(e))
536 | 
537 | @app.get("/blogs/{blog_id}/versions", response_model=APIResponse)
538 | async def get_blog_versions(blog_id: str):
539 |     """Get all versions of a blog."""
540 |     try:
541 |         if blog_id not in blogs_db:
542 |             raise HTTPException(status_code=404, detail="Blog not found")
543 |         
544 |         blog = blogs_db[blog_id]
545 |         versions = list_blog_versions(blog.folder_path)
546 |         
547 |         return APIResponse(
548 |             success=True,
549 |             message="Blog versions retrieved successfully",
550 |             data=versions
551 |         )
552 |     except HTTPException:
553 |         raise
554 |     except Exception as e:
555 |         raise HTTPException(status_code=500, detail=str(e))
556 | 
557 | @app.get("/blogs/{blog_id}/versions/{version_num}/content", response_model=APIResponse)
558 | async def get_blog_version_content(blog_id: str, version_num: int):
559 |     """Get the content of a specific blog version."""
560 |     try:
561 |         if blog_id not in blogs_db:
562 |             raise HTTPException(status_code=404, detail="Blog not found")
563 |         
564 |         blog = blogs_db[blog_id]
565 |         final_folder = Path(blog.folder_path) / "final"
566 |         version_file = final_folder / f"v{version_num}.md"
567 |         
568 |         if not version_file.exists():
569 |             raise HTTPException(status_code=404, detail="Version not found")
570 |         
571 |         with open(version_file, 'r', encoding='utf-8') as f:
572 |             content = f.read()
573 |         
574 |         return APIResponse(
575 |             success=True,
576 |             message="Version content retrieved successfully",
577 |             data={"content": content}
578 |         )
579 |     except HTTPException:
580 |         raise
581 |     except Exception as e:
582 |         raise HTTPException(status_code=500, detail=str(e))
583 | 
584 | @app.put("/blogs/{blog_id}/content", response_model=APIResponse)
585 | async def update_blog_content(blog_id: str, content_data: dict):
586 |     """Update blog content manually."""
587 |     try:
588 |         if blog_id not in blogs_db:
589 |             raise HTTPException(status_code=404, detail="Blog not found")
590 |         
591 |         blog = blogs_db[blog_id]
592 |         new_content = content_data.get("content", "")
593 |         
594 |         if not new_content.strip():
595 |             raise HTTPException(status_code=400, detail="Content cannot be empty")
596 |         
597 |         # Save as new version if this is different from current content
598 |         if blog.latest_content != new_content:
599 |             # Get next version number and save content
600 |             version_number = get_next_version_number(blog.folder_path)
601 |             version_file = save_blog_version(blog.folder_path, new_content, version_number)
602 |             
603 |             # Update blog with new content
604 |             blog.current_version = version_number
605 |             blog.latest_content = new_content
606 |             blog.updated_at = get_current_timestamp()
607 |             blog.status = BlogStatus.IN_PROGRESS
608 |             save_blogs_to_file()  # Save to persistent storage
609 |             
610 |             return APIResponse(
611 |                 success=True,
612 |                 message="Blog content updated successfully",
613 |                 data={
614 |                     "version": version_number,
615 |                     "content": new_content,
616 |                     "file_path": version_file
617 |                 }
618 |             )
619 |         else:
620 |             return APIResponse(
621 |                 success=True,
622 |                 message="No changes detected",
623 |                 data={
624 |                     "version": blog.current_version,
625 |                     "content": blog.latest_content
626 |                 }
627 |             )
628 |             
629 |     except HTTPException:
630 |         raise
631 |     except Exception as e:
632 |         raise HTTPException(status_code=500, detail=str(e))
633 | async def _update_blog_to_highest_version(
634 |     blog: Blog, 
635 |     final_folder: Path, 
636 |     deleted_version: int
637 | ) -> None:
638 |     """Update blog to highest remaining version after deletion.
639 |     
640 |     Args:
641 |         blog: Blog object to update
642 |         final_folder: Path to the final versions folder
643 |         deleted_version: Version number that was deleted
644 |     """
645 |     remaining_versions = list_blog_versions(blog.folder_path)
646 |     if not remaining_versions:
647 |         return
648 |     
649 |     highest_version = max(v["version"] for v in remaining_versions)
650 |     
651 |     # Only update if current version is higher than highest remaining
652 |     if blog.current_version > highest_version:
653 |         blog.current_version = highest_version
654 |         
655 |         # Load content from highest remaining version
656 |         highest_version_file = final_folder / f"v{highest_version}.md"
657 |         try:
658 |             content = await asyncio.to_thread(
659 |                 read_file_content, 
660 |                 str(highest_version_file)
661 |             )
662 |             blog.latest_content = content
663 |         except Exception as e:
664 |             print(f"Warning: Could not load content from v{highest_version}: {e}")
665 |         
666 |         blog.updated_at = get_current_timestamp()
667 |         save_blogs_to_file()
668 | 
669 | 
670 | 
671 | @app.delete("/blogs/{blog_id}/versions/{version_num}", response_model=APIResponse)
672 | async def delete_blog_version(blog_id: str, version_num: int):
673 |     """Delete a specific blog version."""
674 |     try:
675 |         # Validate blog exists
676 |         if blog_id not in blogs_db:
677 |             raise HTTPException(status_code=404, detail="Blog not found")
678 |         
679 |         blog = blogs_db[blog_id]
680 |         final_folder = Path(blog.folder_path) / "final"
681 |         version_file = final_folder / f"v{version_num}.md"
682 |         
683 |         # Validate version exists
684 |         if not await asyncio.to_thread(version_file.exists):
685 |             raise HTTPException(status_code=404, detail="Version not found")
686 |         
687 |         # Prevent deleting current version
688 |         if version_num == blog.current_version:
689 |             raise HTTPException(
690 |                 status_code=400,
691 |                 detail="Cannot delete the current version. Please create a new version first."
692 |             )
693 |         
694 |         # Delete version file asynchronously
695 |         await asyncio.to_thread(version_file.unlink)
696 |         
697 |         # Update blog to highest remaining version if needed
698 |         await _update_blog_to_highest_version(blog, final_folder, version_num)
699 |         
700 |         return APIResponse(
701 |             success=True,
702 |             message=f"Version {version_num} deleted successfully",
703 |             data={
704 |                 "deleted_version": version_num,
705 |                 "current_version": blog.current_version
706 |             }
707 |         )
708 |         
709 |     except HTTPException:
710 |         raise
711 |     except Exception as e:
712 |         raise HTTPException(status_code=500, detail=str(e))
713 | 
714 | @app.post("/blogs/{blog_id}/generate", response_model=APIResponse)
715 | async def generate_blog_content(blog_id: str, request_data: dict):
716 |     """Generate new blog content using IBM watsonx AI."""
717 |     try:
718 |         if blog_id not in blogs_db:
719 |             raise HTTPException(status_code=404, detail="Blog not found")
720 |         
721 |         blog = blogs_db[blog_id]
722 |         prompt = request_data.get("prompt", "")
723 |         generation_type = request_data.get("generation_type", "text")  # Default to text only
724 |         
725 |         if not prompt:
726 |             raise HTTPException(status_code=400, detail="Prompt is required")
727 |             
728 |         # Force text-only generation (images disabled)
729 |         generation_type = "text"
730 |         
731 |         # Get IBM watsonx client
732 |         client = await get_watsonx_client()
733 |         if not client:
734 |             raise HTTPException(status_code=500, detail="IBM watsonx client not initialized")
735 |         
736 |         final_content = ""
737 |         images_generated = False
738 |         text_generated = False
739 |         log_id = ""
740 |         start_time = get_current_timestamp()
741 |         
742 |         try:
743 |             # Generate text content only (images disabled)
744 |             current_content_context = ""
745 |             if blog.latest_content:
746 |                 current_content_context = f"""
747 | 
748 | Current Blog Content:
749 | {blog.latest_content}
750 | 
751 | """
752 |             
753 |             enhanced_prompt = f"""You are an expert blog writer creating high-quality, engaging content for the blog titled: "{blog.title}"
754 |             
755 | Blog Description: {blog.description or "No description provided"}
756 | Tags: {', '.join(blog.tags) if blog.tags else "No tags"}
757 | Publication Site: {blog.publication_site or "General audience"}{current_content_context}
758 | User Request: {prompt}
759 | 
760 | IMPORTANT REQUIREMENTS:
761 | 1. Create professional, well-structured blog content that is engaging, informative, and optimized for the target audience
762 | 2. Use appropriate headings, bullet points, and formatting when relevant
763 | 3. Write in a clear, professional tone suitable for online publication
764 | 4. Focus purely on text content with excellent structure and flow
765 | 5. Create comprehensive, detailed content that stands on its own
766 | 6. Use markdown formatting for headers, lists, and emphasis
767 | 
768 | {f"Based on the current content above, " + prompt if blog.latest_content else prompt}"""
769 |             
770 |             # Log the request with the correct model from config
771 |             from services.watsonx_service.config import granite_config
772 |             log_id = log_watsonx_request(blog_id, enhanced_prompt, granite_config.model_id)
773 |             
774 |             # Generate content with IBM watsonx
775 |             generated_content = client.generate(enhanced_prompt)
776 |             
777 |             if not generated_content:
778 |                 raise Exception("IBM watsonx returned empty response")
779 |             
780 |             text_generated = True
781 |             
782 |             # Calculate processing time and log response
783 |             end_time = get_current_timestamp()
784 |             processing_time_ms = int((end_time - start_time).total_seconds() * 1000)
785 |             log_watsonx_response(log_id, generated_content, "", processing_time_ms)
786 |             
787 |             # Text-only generation (no images)
788 |             final_content = generated_content
789 |             
790 |             # Save the prompt
791 |             save_prompt(blog.folder_path, prompt)
792 |             
793 |             # Get next version number and save content
794 |             version_number = get_next_version_number(blog.folder_path)
795 |             version_file = save_blog_version(blog.folder_path, final_content, version_number)
796 |             
797 |             # Update blog with latest content
798 |             blog.current_version = version_number
799 |             blog.latest_content = final_content
800 |             blog.updated_at = get_current_timestamp()
801 |             blog.status = BlogStatus.IN_PROGRESS
802 |             save_blogs_to_file()  # Save to persistent storage
803 |             
804 |             # Success message for text-only generation
805 |             message = "Blog content generated successfully"
806 |             
807 |             return APIResponse(
808 |                 success=True,
809 |                 message=message,
810 |                 data={
811 |                     "version": version_number,
812 |                     "content": final_content,
813 |                     "file_path": version_file,
814 |                     "generation_type": "text",
815 |                     "text_generated": text_generated,
816 |                     "images_generated": False
817 |                 }
818 |             )
819 |             
820 |         except Exception as ai_error:
821 |             if log_id:
822 |                 end_time = get_current_timestamp()
823 |                 processing_time_ms = int((end_time - start_time).total_seconds() * 1000)
824 |                 log_watsonx_response(log_id, "", str(ai_error), processing_time_ms)
825 |             raise HTTPException(status_code=500, detail=f"AI generation error: {str(ai_error)}")
826 |         
827 |     except HTTPException:
828 |         raise
829 |     except Exception as e:
830 |         raise HTTPException(status_code=500, detail=str(e))
831 | 
832 | @app.post("/blogs/{blog_id}/comments", response_model=APIResponse)
833 | async def add_comment(blog_id: str, comment_data: CommentCreate):
834 |     """Add a comment to a blog."""
835 |     try:
836 |         if blog_id not in blogs_db:
837 |             raise HTTPException(status_code=404, detail="Blog not found")
838 |         
839 |         comment_id = generate_id()
840 |         comment = Comment(
841 |             id=comment_id,
842 |             blog_id=blog_id,
843 |             content=comment_data.content,
844 |             requested_changes=comment_data.requested_changes,
845 |             created_at=get_current_timestamp()
846 |         )
847 |         
848 |         if blog_id not in comments_db:
849 |             comments_db[blog_id] = []
850 |         comments_db[blog_id].append(comment)
851 |         save_comments_to_file()  # Save to persistent storage
852 |         
853 |         return APIResponse(
854 |             success=True,
855 |             message="Comment added successfully",
856 |             data=comment.model_dump(mode='json')
857 |         )
858 |     except HTTPException:
859 |         raise
860 |     except Exception as e:
861 |         raise HTTPException(status_code=500, detail=str(e))
862 | 
863 | @app.get("/blogs/{blog_id}/comments", response_model=APIResponse)
864 | async def get_blog_comments(blog_id: str):
865 |     """Get all comments for a blog."""
866 |     try:
867 |         if blog_id not in blogs_db:
868 |             raise HTTPException(status_code=404, detail="Blog not found")
869 |         
870 |         comments = comments_db.get(blog_id, [])
871 |         comments_list = [comment.model_dump(mode='json') for comment in comments]
872 |         
873 |         return APIResponse(
874 |             success=True,
875 |             message="Comments retrieved successfully",
876 |             data=comments_list
877 |         )
878 |     except HTTPException:
879 |         raise
880 |     except Exception as e:
881 |         raise HTTPException(status_code=500, detail=str(e))
882 | 
883 | if __name__ == "__main__":
884 |     import uvicorn
885 |     uvicorn.run(app, host="0.0.0.0", port=settings.blog_service_port)
</content>
</file>
<file><path>services/ui_service/main.py</path>
<content lines="1-434">
  1 | from fastapi import FastAPI, Request, Form, HTTPException
  2 | from fastapi.responses import HTMLResponse, RedirectResponse
  3 | from fastapi.staticfiles import StaticFiles
  4 | from fastapi.templating import Jinja2Templates
  5 | import httpx
  6 | from pathlib import Path
  7 | import sys
  8 | from typing import Optional, List
  9 | 
 10 | # Add the project root to the Python path
 11 | project_root = Path(__file__).parent.parent.parent
 12 | sys.path.append(str(project_root))
 13 | 
 14 | from shared.config import settings
 15 | 
 16 | app = FastAPI(
 17 |     title="Blog Writer UI",
 18 |     description="Web interface for the blog writer application",
 19 |     version="1.0.0"
 20 | )
 21 | 
 22 | # Set up templates and static files
 23 | templates_dir = Path(__file__).parent / "templates"
 24 | static_dir = Path(__file__).parent / "static"
 25 | 
 26 | # Create directories if they don't exist
 27 | templates_dir.mkdir(exist_ok=True)
 28 | static_dir.mkdir(exist_ok=True)
 29 | 
 30 | templates = Jinja2Templates(directory=str(templates_dir))
 31 | 
 32 | # Mount static files
 33 | app.mount("/static", StaticFiles(directory=str(static_dir)), name="static")
 34 | 
 35 | # Mount generated images directory (create it if it doesn't exist)
 36 | images_dir = project_root / "generated_images"
 37 | images_dir.mkdir(exist_ok=True)
 38 | app.mount("/images", StaticFiles(directory=str(images_dir)), name="images")
 39 | 
 40 | @app.get("/", response_class=HTMLResponse)
 41 | async def home(request: Request):
 42 |     """Home page showing all blogs."""
 43 |     try:
 44 |         # Fetch blogs from API Gateway
 45 |         async with httpx.AsyncClient() as client:
 46 |             response = await client.get(f"http://localhost:{settings.api_gateway_port}/api/blogs")
 47 |             if response.status_code == 200:
 48 |                 blogs_data = response.json()
 49 |                 blogs = blogs_data.get("data", []) if blogs_data.get("success") else []
 50 |             else:
 51 |                 blogs = []
 52 |     except:
 53 |         blogs = []
 54 |     
 55 |     return templates.TemplateResponse("home.html", {
 56 |         "request": request,
 57 |         "blogs": blogs
 58 |     })
 59 | 
 60 | @app.get("/create", response_class=HTMLResponse)
 61 | async def create_blog_page(request: Request):
 62 |     """Blog creation page."""
 63 |     return templates.TemplateResponse("create.html", {"request": request})
 64 | 
 65 | @app.get("/agents", response_class=HTMLResponse)
 66 | async def agent_dashboard(request: Request):
 67 |     """Agent performance dashboard."""
 68 |     return templates.TemplateResponse("agent_dashboard.html", {"request": request})
 69 | 
 70 | @app.post("/create")
 71 | async def create_blog_submit(
 72 |     request: Request,
 73 |     title: str = Form(...),
 74 |     description: str = Form(""),
 75 |     tags: str = Form(""),
 76 |     publication_site: str = Form(""),
 77 |     initial_prompt: str = Form(...),
 78 |     use_orchestration: Optional[str] = Form(None)
 79 | ):
 80 |     """Handle blog creation form submission."""
 81 |     try:
 82 |         # Check if orchestration is enabled
 83 |         if use_orchestration == "true":
 84 |             # Use orchestration service for blog generation
 85 |             async with httpx.AsyncClient(timeout=60.0) as client:
 86 |                 response = await client.post(
 87 |                     f"http://localhost:{settings.api_gateway_port}/api/blogs/generate-orchestrated",
 88 |                     json={
 89 |                         "prompt": initial_prompt,
 90 |                         "blog_id": None,
 91 |                         "tone": "professional"
 92 |                     }
 93 |                 )
 94 |                 
 95 |                 if response.status_code == 200:
 96 |                     return RedirectResponse(url="/?success=Blog generated with orchestration", status_code=303)
 97 |                 else:
 98 |                     error_msg = "Failed to generate blog with orchestration"
 99 |                     return templates.TemplateResponse("create.html", {
100 |                         "request": request,
101 |                         "error": error_msg
102 |                     })
103 |         else:
104 |             # Standard blog creation
105 |             blog_data = {
106 |                 "title": title,
107 |                 "description": description if description else None,
108 |                 "tags": [tag.strip() for tag in tags.split(",") if tag.strip()],
109 |                 "publication_site": publication_site if publication_site else None,
110 |                 "initial_prompt": initial_prompt
111 |             }
112 |             
113 |             # Create blog via API Gateway
114 |             async with httpx.AsyncClient() as client:
115 |                 response = await client.post(
116 |                     f"http://localhost:{settings.api_gateway_port}/api/blogs",
117 |                     json=blog_data
118 |                 )
119 |                 
120 |                 if response.status_code == 200:
121 |                     return RedirectResponse(url="/", status_code=303)
122 |                 else:
123 |                     error_msg = "Failed to create blog"
124 |                     return templates.TemplateResponse("create.html", {
125 |                         "request": request,
126 |                         "error": error_msg
127 |                     })
128 |     except Exception as e:
129 |         return templates.TemplateResponse("create.html", {
130 |             "request": request,
131 |             "error": str(e)
132 |         })
133 | 
134 | @app.get("/blog/{blog_id}", response_class=HTMLResponse)
135 | async def view_blog(request: Request, blog_id: str):
136 |     """View/edit a specific blog."""
137 |     try:
138 |         # Fetch blog details
139 |         async with httpx.AsyncClient() as client:
140 |             blog_response = await client.get(
141 |                 f"http://localhost:{settings.api_gateway_port}/api/blogs/{blog_id}"
142 |             )
143 |             versions_response = await client.get(
144 |                 f"http://localhost:{settings.api_gateway_port}/api/blogs/{blog_id}/versions"
145 |             )
146 |             comments_response = await client.get(
147 |                 f"http://localhost:{settings.api_gateway_port}/api/blogs/{blog_id}/comments"
148 |             )
149 |             
150 |             blog = None
151 |             versions = []
152 |             comments = []
153 |             
154 |             if blog_response.status_code == 200:
155 |                 blog_data = blog_response.json()
156 |                 blog = blog_data.get("data") if blog_data.get("success") else None
157 |             
158 |             if versions_response.status_code == 200:
159 |                 versions_data = versions_response.json()
160 |                 versions = versions_data.get("data", []) if versions_data.get("success") else []
161 |             
162 |             if comments_response.status_code == 200:
163 |                 comments_data = comments_response.json()
164 |                 comments = comments_data.get("data", []) if comments_data.get("success") else []
165 |             
166 |             if not blog:
167 |                 raise HTTPException(status_code=404, detail="Blog not found")
168 |             
169 |             return templates.TemplateResponse("blog_detail.html", {
170 |                 "request": request,
171 |                 "blog": blog,
172 |                 "versions": versions,
173 |                 "comments": comments
174 |             })
175 |     except HTTPException:
176 |         raise
177 |     except Exception as e:
178 |         raise HTTPException(status_code=500, detail=str(e))
179 | 
180 | @app.post("/blog/{blog_id}/generate")
181 | async def generate_content(
182 |     request: Request,
183 |     blog_id: str,
184 |     prompt: str = Form(...),
185 |     generation_type: str = Form("all")  # Default to "all" for backward compatibility
186 | ):
187 |     """Generate new content for a blog."""
188 |     try:
189 |         async with httpx.AsyncClient() as client:
190 |             response = await client.post(
191 |                 f"http://localhost:{settings.api_gateway_port}/api/blogs/{blog_id}/generate",
192 |                 json={"prompt": prompt, "generation_type": generation_type}
193 |             )
194 |             
195 |             if response.status_code == 200:
196 |                 return RedirectResponse(url=f"/blog/{blog_id}", status_code=303)
197 |             else:
198 |                 # Try to get detailed error from response
199 |                 try:
200 |                     error_data = response.json()
201 |                     error_msg = error_data.get("detail", "Failed to generate content")
202 |                 except:
203 |                     error_msg = f"Failed to generate content (HTTP {response.status_code})"
204 |                 return RedirectResponse(url=f"/blog/{blog_id}?error={error_msg}", status_code=303)
205 |     except Exception as e:
206 |         return RedirectResponse(url=f"/blog/{blog_id}?error={str(e)}", status_code=303)
207 | 
208 | @app.post("/blog/{blog_id}/comment")
209 | async def add_comment(
210 |     request: Request,
211 |     blog_id: str,
212 |     content: str = Form(...),
213 |     requested_changes: str = Form("")
214 | ):
215 |     """Add a comment to a blog."""
216 |     try:
217 |         comment_data = {
218 |             "content": content,
219 |             "requested_changes": requested_changes if requested_changes else None
220 |         }
221 |         
222 |         async with httpx.AsyncClient() as client:
223 |             response = await client.post(
224 |                 f"http://localhost:{settings.api_gateway_port}/api/blogs/{blog_id}/comments",
225 |                 json=comment_data
226 |             )
227 |             
228 |             return RedirectResponse(url=f"/blog/{blog_id}", status_code=303)
229 |     except Exception as e:
230 |         return RedirectResponse(url=f"/blog/{blog_id}?error={str(e)}", status_code=303)
231 | 
232 | @app.get("/api/blogs/{blog_id}/versions/{version_num}/content")
233 | async def get_blog_version_content(blog_id: str, version_num: int):
234 |     """Proxy request to get blog version content."""
235 |     try:
236 |         async with httpx.AsyncClient() as client:
237 |             response = await client.get(
238 |                 f"http://localhost:{settings.api_gateway_port}/api/blogs/{blog_id}/versions/{version_num}/content"
239 |             )
240 |             
241 |             if response.status_code == 200:
242 |                 return response.json()
243 |             else:
244 |                 return {"success": False, "message": "Failed to load content"}
245 |     except Exception as e:
246 |         return {"success": False, "message": f"Error: {str(e)}"}
247 | 
248 | @app.put("/api/blogs/{blog_id}/content")
249 | async def update_blog_content(blog_id: str, content_data: dict):
250 |     """Proxy request to update blog content."""
251 |     try:
252 |         async with httpx.AsyncClient() as client:
253 |             response = await client.put(
254 |                 f"http://localhost:{settings.api_gateway_port}/api/blogs/{blog_id}/content",
255 |                 json=content_data
256 |             )
257 |             
258 |             if response.status_code == 200:
259 |                 return response.json()
260 |             else:
261 |                 return {"success": False, "message": "Failed to update content"}
262 |     except Exception as e:
263 |         return {"success": False, "message": f"Error: {str(e)}"}
264 | 
265 | @app.post("/blog/{blog_id}/content")
266 | async def save_blog_content(
267 |     request: Request,
268 |     blog_id: str,
269 |     content: str = Form(...)
270 | ):
271 |     """Save manually edited blog content."""
272 |     try:
273 |         async with httpx.AsyncClient() as client:
274 |             response = await client.put(
275 |                 f"http://localhost:{settings.api_gateway_port}/api/blogs/{blog_id}/content",
276 |                 json={"content": content}
277 |             )
278 |             
279 |             if response.status_code == 200:
280 |                 return RedirectResponse(url=f"/blog/{blog_id}?success=Content saved successfully", status_code=303)
281 |             else:
282 |                 error_msg = "Failed to save content"
283 |                 return RedirectResponse(url=f"/blog/{blog_id}?error={error_msg}", status_code=303)
284 |     except Exception as e:
285 |         return RedirectResponse(url=f"/blog/{blog_id}?error={str(e)}", status_code=303)
286 | 
287 | @app.post("/blog/{blog_id}/versions/{version_num}/delete")
288 | async def delete_blog_version(
289 |     request: Request,
290 |     blog_id: str,
291 |     version_num: int
292 | ):
293 |     """Delete a specific blog version."""
294 |     try:
295 |         async with httpx.AsyncClient() as client:
296 |             response = await client.delete(
297 |                 f"http://localhost:{settings.api_gateway_port}/api/blogs/{blog_id}/versions/{version_num}"
298 |             )
299 |             
300 |             if response.status_code == 200:
301 |                 return RedirectResponse(url=f"/blog/{blog_id}?success=Version {version_num} deleted successfully", status_code=303)
302 |             else:
303 |                 data = response.json() if response.headers.get("content-type", "").startswith("application/json") else {}
304 |                 error_msg = data.get("detail", "Failed to delete version")
305 |                 return RedirectResponse(url=f"/blog/{blog_id}?error={error_msg}", status_code=303)
306 |     except Exception as e:
307 |         return RedirectResponse(url=f"/blog/{blog_id}?error={str(e)}", status_code=303)
308 | 
309 | @app.get("/settings", response_class=HTMLResponse)
310 | async def settings_page(request: Request):
311 |     """Settings page."""
312 |     try:
313 |         # Fetch current settings
314 |         async with httpx.AsyncClient() as client:
315 |             response = await client.get(
316 |                 f"http://localhost:{settings.settings_service_port}/settings"
317 |             )
318 |             
319 |             current_settings = {}
320 |             if response.status_code == 200:
321 |                 settings_data = response.json()
322 |                 current_settings = settings_data.get("data", {}) if settings_data.get("success") else {}
323 |             
324 |             return templates.TemplateResponse("settings.html", {
325 |                 "request": request,
326 |                 "settings": current_settings
327 |             })
328 |     except Exception as e:
329 |         return templates.TemplateResponse("settings.html", {
330 |             "request": request,
331 |             "error": str(e),
332 |             "settings": {}
333 |         })
334 | 
335 | @app.post("/settings")
336 | async def update_settings(
337 |     request: Request,
338 |     ibm_cloud_api_key: str = Form(""),
339 |     watsonx_project_id: str = Form(""),
340 |     watsonx_url: str = Form("https://us-south.ml.cloud.ibm.com"),
341 |     watsonx_model_id: str = Form("meta-llama/llama-3-3-70b-instruct"),
342 |     source_folder: str = Form(""),
343 |     default_publication_site: str = Form("")
344 | ):
345 |     """Update settings."""
346 |     try:
347 |         settings_data = {}
348 |         
349 |         if ibm_cloud_api_key:
350 |             settings_data["ibm_cloud_api_key"] = ibm_cloud_api_key
351 |         if watsonx_project_id:
352 |             settings_data["watsonx_project_id"] = watsonx_project_id
353 |         if watsonx_url:
354 |             settings_data["watsonx_url"] = watsonx_url
355 |         if watsonx_model_id:
356 |             settings_data["watsonx_model_id"] = watsonx_model_id
357 |         if source_folder:
358 |             settings_data["source_folder"] = source_folder
359 |         if default_publication_site:
360 |             settings_data["default_publication_site"] = default_publication_site
361 |         
362 |         async with httpx.AsyncClient() as client:
363 |             response = await client.put(
364 |                 f"http://localhost:{settings.settings_service_port}/settings",
365 |                 json=settings_data
366 |             )
367 |             
368 |             if response.status_code == 200:
369 |                 return RedirectResponse(url="/settings?success=1", status_code=303)
370 |             else:
371 |                 return RedirectResponse(url="/settings?error=Failed to update settings", status_code=303)
372 |     except Exception as e:
373 |         return RedirectResponse(url=f"/settings?error={str(e)}", status_code=303)
374 | 
375 | @app.get("/watsonx-logs", response_class=HTMLResponse)
376 | async def watsonx_logs_page(request: Request, page: int = 1):
377 |     """WatsonX API logs page with pagination."""
378 |     try:
379 |         # Fetch WatsonX logs from blog service
380 |         async with httpx.AsyncClient() as client:
381 |             response = await client.get(
382 |                 f"http://localhost:{settings.blog_service_port}/watsonx-logs?page={page}&page_size=10"
383 |             )
384 |             
385 |             logs_data = []
386 |             pagination = {}
387 |             
388 |             if response.status_code == 200:
389 |                 data = response.json()
390 |                 if data.get("success"):
391 |                     logs_data = data.get("data", {}).get("logs", [])
392 |                     pagination = data.get("data", {}).get("pagination", {})
393 |             
394 |             return templates.TemplateResponse("watsonx_logs.html", {
395 |                 "request": request,
396 |                 "logs": logs_data,
397 |                 "pagination": pagination
398 |             })
399 |     except Exception as e:
400 |         return templates.TemplateResponse("watsonx_logs.html", {
401 |             "request": request,
402 |             "error": str(e),
403 |             "logs": [],
404 |             "pagination": {}
405 |         })
406 | 
407 | @app.get("/imagen-logs", response_class=HTMLResponse)
408 | async def imagen_logs_page(request: Request, page: int = 1):
409 |     """Image generation logs page (deprecated feature)."""
410 |     try:
411 |         # Return empty page as feature is deprecated
412 |         return templates.TemplateResponse("imagen_logs.html", {
413 |             "request": request,
414 |             "logs": [],
415 |             "pagination": {
416 |                 "current_page": 1,
417 |                 "page_size": 10,
418 |                 "total_logs": 0,
419 |                 "total_pages": 0,
420 |                 "has_next": False,
421 |                 "has_prev": False
422 |             }
423 |         })
424 |     except Exception as e:
425 |         return templates.TemplateResponse("imagen_logs.html", {
426 |             "request": request,
427 |             "error": str(e),
428 |             "logs": [],
429 |             "pagination": {}
430 |         })
431 | 
432 | if __name__ == "__main__":
433 |     import uvicorn
434 |     uvicorn.run(app, host="0.0.0.0", port=settings.ui_service_port)
</content>
</file>
<file><path>shared/models.py</path>
<content lines="1-137">
  1 | from pydantic import BaseModel
  2 | from typing import Optional, List, Dict, Any
  3 | from datetime import datetime
  4 | from enum import Enum
  5 | 
  6 | 
  7 | class PublicationSite(str, Enum):
  8 |     MEDIUM = "medium"
  9 |     WORDPRESS = "wordpress"
 10 |     GHOST = "ghost"
 11 |     CUSTOM = "custom"
 12 | 
 13 | 
 14 | class BlogStatus(str, Enum):
 15 |     DRAFT = "draft"
 16 |     IN_PROGRESS = "in_progress"
 17 |     REVIEW = "review"
 18 |     COMPLETED = "completed"
 19 |     PUBLISHED = "published"
 20 | 
 21 | 
 22 | class BlogBase(BaseModel):
 23 |     title: str
 24 |     description: Optional[str] = None
 25 |     tags: List[str] = []
 26 |     publication_site: Optional[PublicationSite] = None
 27 | 
 28 | 
 29 | class BlogCreate(BlogBase):
 30 |     initial_prompt: str
 31 | 
 32 | 
 33 | class BlogUpdate(BaseModel):
 34 |     title: Optional[str] = None
 35 |     description: Optional[str] = None
 36 |     tags: Optional[List[str]] = None
 37 |     publication_site: Optional[PublicationSite] = None
 38 |     status: Optional[BlogStatus] = None
 39 | 
 40 | 
 41 | class Blog(BlogBase):
 42 |     id: str
 43 |     status: BlogStatus
 44 |     created_at: datetime
 45 |     updated_at: datetime
 46 |     folder_path: str
 47 |     current_version: int
 48 |     latest_content: Optional[str] = None  # Store the latest generated content
 49 |     
 50 |     class Config:
 51 |         from_attributes = True
 52 | 
 53 | 
 54 | class BlogVersion(BaseModel):
 55 |     id: str
 56 |     blog_id: str
 57 |     version_number: int
 58 |     content: str
 59 |     prompt_used: str
 60 |     created_at: datetime
 61 |     created_by: str = "system"
 62 |     
 63 |     class Config:
 64 |         from_attributes = True
 65 | 
 66 | 
 67 | class CommentCreate(BaseModel):
 68 |     content: str
 69 |     requested_changes: Optional[str] = None
 70 | 
 71 | 
 72 | class Comment(BaseModel):
 73 |     id: str
 74 |     blog_id: str
 75 |     content: str
 76 |     requested_changes: Optional[str] = None
 77 |     created_at: datetime
 78 |     
 79 |     class Config:
 80 |         from_attributes = True
 81 | 
 82 | 
 83 | class SettingsBase(BaseModel):
 84 |     source_folder: Optional[str] = None
 85 |     default_publication_site: Optional[PublicationSite] = None
 86 |     
 87 |     # IBM watsonx.ai Configuration
 88 |     ibm_cloud_api_key: Optional[str] = None
 89 |     watsonx_project_id: Optional[str] = None
 90 |     watsonx_url: str = "https://us-south.ml.cloud.ibm.com"
 91 |     watsonx_model_id: str = "meta-llama/llama-3-3-70b-instruct"
 92 | 
 93 | 
 94 | class SettingsCreate(SettingsBase):
 95 |     pass
 96 | 
 97 | 
 98 | class SettingsUpdate(SettingsBase):
 99 |     pass
100 | 
101 | 
102 | class Settings(SettingsBase):
103 |     id: str
104 |     created_at: datetime
105 |     updated_at: datetime
106 |     
107 |     class Config:
108 |         from_attributes = True
109 | 
110 | 
111 | class WatsonxAPILog(BaseModel):
112 |     id: str
113 |     request_timestamp: datetime
114 |     blog_id: Optional[str] = None
115 |     prompt: str
116 |     model_used: str
117 |     response_content: Optional[str] = None
118 |     response_timestamp: Optional[datetime] = None
119 |     success: bool
120 |     error_message: Optional[str] = None
121 |     processing_time_ms: Optional[int] = None
122 |     
123 |     class Config:
124 |         from_attributes = True
125 | 
126 | 
127 | class APIResponse(BaseModel):
128 |     success: bool
129 |     message: str
130 |     data: Optional[Any] = None
131 | 
132 | 
133 | class ErrorResponse(BaseModel):
134 |     success: bool = False
135 |     message: str
136 |     error_code: Optional[str] = None
137 |     details: Optional[Dict[str, Any]] = None
</content>
</file>
</files>
<environment_details>
# VSCode Visible Files
services\orchestration_service\agents\writer_agent.py

# VSCode Open Tabs
.vscode/settings.json,services/ui_service/templates/home.html,.bobalytics.json,.gitignore,services/orchestration_service/agent_base.py,services/orchestration_service/agents/publisher_agent.py,services/orchestration_service/agent_registry.py,services/orchestration_service/agents/writer_agent.py,stop_all_services.py,services/ui_service/main.py,services/orchestration_service/main.py,services/ui_service/templates/agent_dashboard.html,services/orchestration_service/pipeline_manager.py,test_agent_metadata.py,test_orchestration.py,enhancement1_B_delta_agent_dashboard.md,services/ui_service/templates/base.html,services/ui_service/templates/create.html,services/api_gateway/main.py,services/orchestration_service/agents/__init__.py

# Actively Running Terminals
## Terminal 1 (Active)
### Working Directory: `c:\workspace\ForgeByBob`
### Original command: `python start_all_services.py`
## Terminal 2 (Active)
### Working Directory: `c:\workspace\ForgeByBob`
### Original command: `python start_all_services.py`
## Terminal 3 (Active)
### Working Directory: `c:\workspace\ForgeByBob`
### Original command: `python start_all_services.py`
## Terminal 4 (Active)
### Working Directory: `c:\workspace\ForgeByBob`
### Original command: `python start_all_services.py`
## Terminal 5 (Active)
### Working Directory: `c:\workspace\ForgeByBob`
### Original command: `python start_all_services.py`
## Terminal 6 (Active)
### Working Directory: `c:\workspace\ForgeByBob`
### Original command: `python start_all_services.py`
## Terminal 7 (Active)
### Working Directory: `c:\workspace\ForgeByBob`
### Original command: `python stop_all_services.py; python start_all_services.py`
## Terminal 8 (Active)
### Working Directory: `c:\workspace\ForgeByBob`
### Original command: `python stop_all_services.py; Start-Sleep -Seconds 3; python start_all_services.py`

# Current Time
Current time in ISO 8601 UTC format: 2026-05-02T08:17:09.385Z
User time zone: America/New_York, UTC-4:00

# Current Cost
$0.01

# Review Exclusions
The following file patterns are excluded from code reviews:
- .vscode/**

# Current Mode
<slug>code</slug>
<name>💻 Code</name>
You have not created a todo list yet. Create one with `update_todo_list` if your task is complicated or involves multiple steps.
</environment_details>

---

**Assistant:**

I can see the issue. The error "Failed to create blog: 422" indicates a validation error. Looking at the code, I can see that in `services/blog_service/main.py`, the `BlogCreate` model expects an `initial_prompt` field, but the `publication_site` field in the model is typed as `Optional[PublicationSite]` (an Enum), while the UI is sending it as a string.

Let me check the create.html template to see what's being sent:

<read_file>
<args>
<file>
<path>services/ui_service/templates/create.html</path>
</file>
</args>
</read_file>

---

**User:**

[read_file for 'services/ui_service/templates/create.html'. Reading multiple files at once is more efficient for the LLM. If other files are relevant to your current task, please read them simultaneously.] Result:
<files>
<file><path>services/ui_service/templates/create.html</path>
<content lines="1-80">
 1 | {% extends "base.html" %}
 2 | 
 3 | {% block title %}Create New Blog - IBM watsonx.ai{% endblock %}
 4 | 
 5 | {% block content %}
 6 | <h2>Create New Blog with IBM watsonx.ai</h2>
 7 | 
 8 | {% if error %}
 9 | <div class="alert alert-error">
10 |     {{ error }}
11 | </div>
12 | {% endif %}
13 | 
14 | <div class="card">
15 |     <form method="post" action="/create">
16 |         <div class="form-group">
17 |             <label for="title">Blog Title *</label>
18 |             <input type="text" id="title" name="title" required>
19 |         </div>
20 |         
21 |         <div class="form-group">
22 |             <label for="description">Description (optional)</label>
23 |             <textarea id="description" name="description" placeholder="Brief description of your blog..."></textarea>
24 |         </div>
25 |         
26 |         <div class="form-group">
27 |             <label for="tags">Tags (comma-separated)</label>
28 |             <input type="text" id="tags" name="tags" placeholder="technology, AI, programming">
29 |         </div>
30 |         
31 |         <div class="form-group">
32 |             <label for="publication_site">Publication Site (optional)</label>
33 |             <select id="publication_site" name="publication_site">
34 |                 <option value="">Select publication site...</option>
35 |                 <option value="medium">Medium</option>
36 |                 <option value="wordpress">WordPress</option>
37 |                 <option value="ghost">Ghost</option>
38 |                 <option value="custom">Custom</option>
39 |             </select>
40 |         </div>
41 |         
42 |         <div class="form-group">
43 |             <label for="initial_prompt">Initial Prompt for IBM watsonx.ai *</label>
44 |             <textarea id="initial_prompt" name="initial_prompt" required placeholder="Describe what you want your blog to be about. Be specific about the topic, target audience, tone, and any key points you want to cover..."></textarea>
45 |             <p style="font-size: 0.9rem; color: #666; margin-top: 0.5rem;">
46 |                 💡 IBM watsonx.ai will use this prompt to generate your initial blog content.
47 |             </p>
48 |         </div>
49 |         
50 |         <div style="margin-bottom: 1.5rem; padding: 1rem; background: #e8f4f8; border-radius: 8px; border: 1px solid #3498db;">
51 |             <label style="display: flex; align-items: center; cursor: pointer;">
52 |                 <input type="checkbox" name="use_orchestration" value="true" style="margin-right: 0.5rem; width: 18px; height: 18px;">
53 |                 <div>
54 |                     <strong style="color: #2c3e50;">🤖 Use Agentic AI Orchestration</strong>
55 |                     <p style="margin: 0.25rem 0 0 0; font-size: 0.9rem; color: #666;">
56 |                         Enable multi-agent workflow with Writer → Publisher pipeline
57 |                     </p>
58 |                 </div>
59 |             </label>
60 |         </div>
61 |         
62 |         <div class="form-group">
63 |             <button type="submit" class="btn btn-primary">Create Blog</button>
64 |             <a href="/" class="btn" style="margin-left: 1rem; background: #95a5a6;">Cancel</a>
65 |         </div>
66 |     </form>
67 | </div>
68 | 
69 | <div class="card" style="margin-top: 2rem; background: #e8f4f8; border-left: 4px solid #3498db;">
70 |     <h4>💡 Tips for Writing Effective Prompts for IBM watsonx.ai:</h4>
71 |     <ul style="margin-left: 2rem; margin-top: 1rem; line-height: 1.8;">
72 |         <li><strong>Be specific</strong> about your topic and target audience</li>
73 |         <li><strong>Mention the desired tone</strong> (professional, casual, informative, technical, etc.)</li>
74 |         <li><strong>Include key points</strong> or sections you want covered</li>
75 |         <li><strong>Specify the length</strong> or format you prefer (e.g., "800-word article", "5-section guide")</li>
76 |         <li><strong>Add requirements</strong> like SEO keywords, specific examples, or constraints</li>
77 |         <li><strong>Note:</strong> Free tier has rate limits - wait 5 minutes between generations if needed</li>
78 |     </ul>
79 | </div>
80 | {% endblock %}
</content>
</file>
</files>
<environment_details>
# VSCode Visible Files
services\orchestration_service\agents\writer_agent.py

# VSCode Open Tabs
.vscode/settings.json,services/ui_service/templates/home.html,.bobalytics.json,.gitignore,services/orchestration_service/agent_base.py,services/orchestration_service/agents/publisher_agent.py,services/orchestration_service/agent_registry.py,services/orchestration_service/agents/writer_agent.py,stop_all_services.py,services/ui_service/main.py,services/orchestration_service/main.py,services/ui_service/templates/agent_dashboard.html,services/orchestration_service/pipeline_manager.py,test_agent_metadata.py,test_orchestration.py,enhancement1_B_delta_agent_dashboard.md,services/ui_service/templates/base.html,services/ui_service/templates/create.html,services/api_gateway/main.py,services/orchestration_service/agents/__init__.py

# Actively Running Terminals
## Terminal 1 (Active)
### Working Directory: `c:\workspace\ForgeByBob`
### Original command: `python start_all_services.py`
## Terminal 2 (Active)
### Working Directory: `c:\workspace\ForgeByBob`
### Original command: `python start_all_services.py`
## Terminal 3 (Active)
### Working Directory: `c:\workspace\ForgeByBob`
### Original command: `python start_all_services.py`
## Terminal 4 (Active)
### Working Directory: `c:\workspace\ForgeByBob`
### Original command: `python start_all_services.py`
## Terminal 5 (Active)
### Working Directory: `c:\workspace\ForgeByBob`
### Original command: `python start_all_services.py`
## Terminal 6 (Active)
### Working Directory: `c:\workspace\ForgeByBob`
### Original command: `python start_all_services.py`
## Terminal 7 (Active)
### Working Directory: `c:\workspace\ForgeByBob`
### Original command: `python stop_all_services.py; python start_all_services.py`
## Terminal 8 (Active)
### Working Directory: `c:\workspace\ForgeByBob`
### Original command: `python stop_all_services.py; Start-Sleep -Seconds 3; python start_all_services.py`

# Current Time
Current time in ISO 8601 UTC format: 2026-05-02T08:17:20.820Z
User time zone: America/New_York, UTC-4:00

# Current Cost
$0.09

# Review Exclusions
The following file patterns are excluded from code reviews:
- .vscode/**

# Current Mode
<slug>code</slug>
<name>💻 Code</name>
You have not created a todo list yet. Create one with `update_todo_list` if your task is complicated or involves multiple steps.
</environment_details>

---

**Assistant:**

I found the issue! The problem is in `services/ui_service/main.py`. When the form sends an empty string for `publication_site`, the code is passing it as an empty string to the API, but the `BlogCreate` model expects either `None` or a valid `PublicationSite` enum value.

The issue is on line 109 of `services/ui_service/main.py`:

```python
"publication_site": publication_site if publication_site else None,
```

This should handle empty strings, but the form is sending an empty string `""` which is truthy in the conditional check. Let me fix this:

<apply_diff>
<path>services/ui_service/main.py</path>
<diff>
<<<<<<< SEARCH
:start_line:104
-------
            # Standard blog creation
            blog_data = {
                "title": title,
                "description": description if description else None,
                "tags": [tag.strip() for tag in tags.split(",") if tag.strip()],
                "publication_site": publication_site if publication_site else None,
                "initial_prompt": initial_prompt
            }
=======
            # Standard blog creation
            blog_data = {
                "title": title,
                "description": description.strip() if description and description.strip() else None,
                "tags": [tag.strip() for tag in tags.split(",") if tag.strip()],
                "publication_site": publication_site.strip() if publication_site and publication_site.strip() else None,
                "initial_prompt": initial_prompt
            }
>>>>>>> REPLACE
</diff>
</apply_diff>

---

**User:**

[apply_diff for 'services/ui_service/main.py'] Result:
<file_write_result>
<path>services/ui_service/main.py</path>
<operation>modified</operation>
<notice>
<i>You do not need to re-read the file, as you have seen all changes</i>
<i>Proceed with the task using these changes as the new baseline.</i>
</notice>
</file_write_result>

<notice>Making multiple related changes in a single apply_diff is more efficient. If other changes are needed in this file, please include them as additional SEARCH/REPLACE blocks.</notice>
<environment_details>
# VSCode Visible Files
services\ui_service\main.py

# VSCode Open Tabs
.vscode/settings.json,services/ui_service/templates/home.html,.bobalytics.json,.gitignore,services/orchestration_service/agent_base.py,services/orchestration_service/agents/publisher_agent.py,services/orchestration_service/agent_registry.py,services/orchestration_service/agents/writer_agent.py,services/ui_service/main.py,stop_all_services.py,services/orchestration_service/main.py,services/ui_service/templates/agent_dashboard.html,services/orchestration_service/pipeline_manager.py,test_agent_metadata.py,test_orchestration.py,enhancement1_B_delta_agent_dashboard.md,services/ui_service/templates/base.html,services/ui_service/templates/create.html,services/api_gateway/main.py,services/orchestration_service/agents/__init__.py

# Recently Modified Files
These files have been modified since you last accessed them (file was just edited so you may need to re-read it before editing):
services/ui_service/main.py

# Actively Running Terminals
## Terminal 1 (Active)
### Working Directory: `c:\workspace\ForgeByBob`
### Original command: `python start_all_services.py`
## Terminal 2 (Active)
### Working Directory: `c:\workspace\ForgeByBob`
### Original command: `python start_all_services.py`
## Terminal 3 (Active)
### Working Directory: `c:\workspace\ForgeByBob`
### Original command: `python start_all_services.py`
## Terminal 4 (Active)
### Working Directory: `c:\workspace\ForgeByBob`
### Original command: `python start_all_services.py`
## Terminal 5 (Active)
### Working Directory: `c:\workspace\ForgeByBob`
### Original command: `python start_all_services.py`
## Terminal 6 (Active)
### Working Directory: `c:\workspace\ForgeByBob`
### Original command: `python start_all_services.py`
## Terminal 7 (Active)
### Working Directory: `c:\workspace\ForgeByBob`
### Original command: `python stop_all_services.py; python start_all_services.py`
## Terminal 8 (Active)
### Working Directory: `c:\workspace\ForgeByBob`
### Original command: `python stop_all_services.py; Start-Sleep -Seconds 3; python start_all_services.py`

# Current Time
Current time in ISO 8601 UTC format: 2026-05-02T08:17:36.260Z
User time zone: America/New_York, UTC-4:00

# Current Cost
$0.17

# Review Exclusions
The following file patterns are excluded from code reviews:
- .vscode/**

# Current Mode
<slug>code</slug>
<name>💻 Code</name>
You have not created a todo list yet. Create one with `update_todo_list` if your task is complicated or involves multiple steps.
</environment_details>

---

**Assistant:**

Now I need to restart the UI service for the changes to take effect. Let me restart the services:

<execute_command>
<command>python stop_all_services.py</command>
</execute_command>

---

**User:**

[execute_command for 'python stop_all_services.py'] Result:
Command executed in terminal  within working directory 'c:/workspace/ForgeByBob'. Exit code: 0
Output:
C:\workspace\ForgeByBob\stop_all_services.py:13: DeprecationWarning: connections() is deprecated and will be removed; use net_connections() instead
  for conn in proc.connections():
=== Stopping All Services ===
Killing python3.13.exe (PID: 16664) on port 8000
[OK] Stopped service on port 8000
Killing python3.13.exe (PID: 12664) on port 8001
[OK] Stopped service on port 8001
Killing python3.13.exe (PID: 16772) on port 8002
[OK] Stopped service on port 8002
Killing System Idle Process (PID: 0) on port 8003
Killing python3.13.exe (PID: 11052) on port 8003
[OK] Stopped service on port 8003
Killing System Idle Process (PID: 0) on port 8004
Killing python3.13.exe (PID: 19100) on port 8004
[OK] Stopped service on port 8004

Waiting for processes to terminate...
[OK] All services stopped!

<environment_details>
# VSCode Visible Files
services\ui_service\main.py

# VSCode Open Tabs
.vscode/settings.json,services/ui_service/templates/home.html,.bobalytics.json,.gitignore,services/orchestration_service/agent_base.py,services/orchestration_service/agents/publisher_agent.py,services/orchestration_service/agent_registry.py,services/orchestration_service/agents/writer_agent.py,services/ui_service/main.py,stop_all_services.py,services/orchestration_service/main.py,services/ui_service/templates/agent_dashboard.html,services/orchestration_service/pipeline_manager.py,test_agent_metadata.py,test_orchestration.py,enhancement1_B_delta_agent_dashboard.md,services/ui_service/templates/base.html,services/ui_service/templates/create.html,services/api_gateway/main.py,services/orchestration_service/agents/__init__.py

# Actively Running Terminals
## Terminal 1 (Active)
### Working Directory: `c:\workspace\ForgeByBob`
### Original command: `python start_all_services.py`
## Terminal 2 (Active)
### Working Directory: `c:\workspace\ForgeByBob`
### Original command: `python start_all_services.py`
## Terminal 3 (Active)
### Working Directory: `c:\workspace\ForgeByBob`
### Original command: `python start_all_services.py`
## Terminal 4 (Active)
### Working Directory: `c:\workspace\ForgeByBob`
### Original command: `python start_all_services.py`
## Terminal 5 (Active)
### Working Directory: `c:\workspace\ForgeByBob`
### Original command: `python start_all_services.py`
## Terminal 6 (Active)
### Working Directory: `c:\workspace\ForgeByBob`
### Original command: `python start_all_services.py`
## Terminal 7 (Active)
### Working Directory: `c:\workspace\ForgeByBob`
### Original command: `python stop_all_services.py; python start_all_services.py`
## Terminal 8 (Active)
### Working Directory: `c:\workspace\ForgeByBob`
### Original command: `python stop_all_services.py; Start-Sleep -Seconds 3; python start_all_services.py`

# Current Time
Current time in ISO 8601 UTC format: 2026-05-02T08:17:52.979Z
User time zone: America/New_York, UTC-4:00

# Current Cost
$0.25

# Review Exclusions
The following file patterns are excluded from code reviews:
- .vscode/**

# Current Mode
<slug>code</slug>
<name>💻 Code</name>
You have not created a todo list yet. Create one with `update_todo_list` if your task is complicated or involves multiple steps.
</environment_details>

---

**Assistant:**

<execute_command>
<command>python start_all_services.py</command>
</execute_command>

---

**User:**

[execute_command for 'python start_all_services.py'] Result:
Command executed in terminal  within working directory 'c:/workspace/ForgeByBob'. Process terminated by signal SIGKILL
Output:
INFO:     Started server process [11756]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8002 (Press CTRL+C to quit)
INFO:     Started server process [11588]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
INFO:     Started server process [21020]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8001 (Press CTRL+C to quit)
C:\workspace\ForgeByBob\services\orchestration_service\main.py:57: DeprecationWarning: 
        on_event is deprecated, use lifespan event handlers instead.

        Read more about it in the
        [FastAPI docs for Lifespan Events](https://fastapi.tiangolo.com/advanced/events/).
        
  @app.on_event("startup")
INFO:     Started server process [21680]
INFO:     Waiting for application startup.
INFO:__main__:Registering agents...
INFO:services.orchestration_service.agent_registry:Registered agent class: writer
INFO:services.orchestration_service.agent_registry:Registered agent class: publisher
INFO:__main__:Agents registered successfully
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8004 (Press CTRL+C to quit)
INFO:     Started server process [22168]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8003 (Press CTRL+C to quit)
Loaded 1 blogs from persistent storage
Loaded 3 WatsonX API logs from persistent storage
INFO:     127.0.0.1:63168 - "GET /blogs HTTP/1.1" 200 OK
INFO:     127.0.0.1:52840 - "GET /api/blogs HTTP/1.1" 200 OK
INFO:     127.0.0.1:62868 - "GET / HTTP/1.1" 200 OK
INFO:     127.0.0.1:62868 - "GET /.well-known/appspecific/com.chrome.devtools.json HTTP/1.1" 404 Not Found
INFO:     127.0.0.1:62868 - "GET /agents HTTP/1.1" 200 OK
INFO:     127.0.0.1:62868 - "GET /.well-known/appspecific/com.chrome.devtools.json HTTP/1.1" 404 Not Found
INFO:     127.0.0.1:54477 - "GET /metrics HTTP/1.1" 200 OK
INFO:     127.0.0.1:54477 - "GET /pipelines HTTP/1.1" 200 OK
INFO:     127.0.0.1:54477 - "GET /agents HTTP/1.1" 200 OK
INFO:     127.0.0.1:54477 - "GET /metrics HTTP/1.1" 200 OK
INFO:     127.0.0.1:54477 - "GET /pipelines HTTP/1.1" 200 OK
INFO:     127.0.0.1:54477 - "GET /agents HTTP/1.1" 200 OK
INFO:     127.0.0.1:54477 - "GET /metrics HTTP/1.1" 200 OK
INFO:     127.0.0.1:54477 - "GET /pipelines HTTP/1.1" 200 OK
INFO:     127.0.0.1:54477 - "GET /agents HTTP/1.1" 200 OK
INFO:     127.0.0.1:54477 - "GET /metrics HTTP/1.1" 200 OK
INFO:     127.0.0.1:54477 - "GET /pipelines HTTP/1.1" 200 OK
INFO:     127.0.0.1:54477 - "GET /agents HTTP/1.1" 200 OK
INFO:     127.0.0.1:54477 - "GET /metrics HTTP/1.1" 200 OK
INFO:     127.0.0.1:54477 - "GET /pipelines HTTP/1.1" 200 OK
INFO:     127.0.0.1:54477 - "GET /agents HTTP/1.1" 200 OK
INFO:     127.0.0.1:54477 - "GET /metrics HTTP/1.1" 200 OK
INFO:     127.0.0.1:54477 - "GET /pipelines HTTP/1.1" 200 OK
INFO:     127.0.0.1:54477 - "GET /agents HTTP/1.1" 200 OK
INFO:     127.0.0.1:54477 - "GET /metrics HTTP/1.1" 200 OK
INFO:     127.0.0.1:54477 - "GET /pipelines HTTP/1.1" 200 OK
INFO:     127.0.0.1:54477 - "GET /agents HTTP/1.1" 200 OK
INFO:services.orchestration_service.agent_base:Agent initialized: WriterAgent (597ffe0b-95a8-461a-98cf-7816c02d7242)
INFO:httpx:HTTP Request: POST https://iam.cloud.ibm.com/identity/token "HTTP/1.1 200 OK"
INFO:ibm_watsonx_ai.client:Client successfully initialized
INFO:httpx:HTTP Request: GET https://api.dataplatform.cloud.ibm.com/v2/projects/your_watsonx_project_id_here "HTTP/1.1 200 OK"
INFO:httpx:HTTP Request: GET https://us-south.ml.cloud.ibm.com/ml/v1/foundation_model_specs?version=2026-04-20&project_id=your_watsonx_project_id_here&filters=%21lifecycle_withdrawn&limit=200 "HTTP/1.1 200 OK"
INFO:ibm_watsonx_ai.wml_resource:Successfully finished Get available foundation models for url: 'https://us-south.ml.cloud.ibm.com/ml/v1/foundation_model_specs?version=2026-04-20&project_id=your_watsonx_project_id_here&filters=%21lifecycle_withdrawn&limit=200'
INFO:services.watsonx_service.granite_client:watsonx client initialized with model: ibm/granite-4-h-small
INFO:services.orchestration_service.agent_registry:Created agent: writer (597ffe0b-95a8-461a-98cf-7816c02d7242)
INFO:services.orchestration_service.agent_base:WriterAgent: Starting execution 94a11299-6fe7-46b4-95b4-8507f5279a71
INFO:services.orchestration_service.agents.writer_agent:WriterAgent: Generating content for prompt: IBM Bob...
INFO:services.orchestration_service.agents.writer_agent:WriterAgent: Creating draft blog via API...
INFO:     127.0.0.1:49237 - "GET /metrics HTTP/1.1" 200 OK
INFO:     127.0.0.1:49237 - "GET /pipelines HTTP/1.1" 200 OK
INFO:     127.0.0.1:49237 - "GET /agents HTTP/1.1" 200 OK
INFO:     127.0.0.1:50102 - "POST /blogs HTTP/1.1" 422 Unprocessable Content
INFO:httpx:HTTP Request: POST http://localhost:8001/blogs "HTTP/1.1 422 Unprocessable Content"
ERROR:services.orchestration_service.agents.writer_agent:WriterAgent: Failed to create blog: 422
INFO:services.orchestration_service.agent_base:WriterAgent: Execution 94a11299-6fe7-46b4-95b4-8507f5279a71 failed
INFO:     127.0.0.1:54477 - "POST /agents/writer/run HTTP/1.1" 200 OK
INFO:     127.0.0.1:54477 - "GET /metrics HTTP/1.1" 200 OK
INFO:     127.0.0.1:54477 - "GET /pipelines HTTP/1.1" 200 OK
INFO:     127.0.0.1:54477 - "GET /agents HTTP/1.1" 200 OK
INFO:     127.0.0.1:54477 - "GET /metrics HTTP/1.1" 200 OK
INFO:     127.0.0.1:54477 - "GET /pipelines HTTP/1.1" 200 OK
INFO:     127.0.0.1:54477 - "GET /agents HTTP/1.1" 200 OK
INFO:     127.0.0.1:54477 - "GET /metrics HTTP/1.1" 200 OK
INFO:     127.0.0.1:54477 - "GET /pipelines HTTP/1.1" 200 OK
INFO:     127.0.0.1:54477 - "GET /agents HTTP/1.1" 200 OK
INFO:     127.0.0.1:54477 - "GET /metrics HTTP/1.1" 200 OK
INFO:     127.0.0.1:54477 - "GET /pipelines HTTP/1.1" 200 OK
INFO:     127.0.0.1:54477 - "GET /agents HTTP/1.1" 200 OK
INFO:     127.0.0.1:54477 - "GET /metrics HTTP/1.1" 200 OK
INFO:     127.0.0.1:54477 - "GET /pipelines HTTP/1.1" 200 OK
INFO:     127.0.0.1:54477 - "GET /agents HTTP/1.1" 200 OK
INFO:     127.0.0.1:54477 - "GET /metrics HTTP/1.1" 200 OK
INFO:     127.0.0.1:54477 - "GET /pipelines HTTP/1.1" 200 OK
INFO:     127.0.0.1:54477 - "GET /agents HTTP/1.1" 200 OK
INFO:     127.0.0.1:54477 - "GET /metrics HTTP/1.1" 200 OK
INFO:     127.0.0.1:54477 - "GET /pipelines HTTP/1.1" 200 OK
INFO:     127.0.0.1:54477 - "GET /agents HTTP/1.1" 200 OK

<environment_details>
# VSCode Visible Files
services\ui_service\main.py

# VSCode Open Tabs
.vscode/settings.json,services/ui_service/templates/home.html,.bobalytics.json,.gitignore,services/orchestration_service/agent_base.py,services/orchestration_service/agents/publisher_agent.py,services/orchestration_service/agent_registry.py,services/orchestration_service/agents/writer_agent.py,services/ui_service/main.py,stop_all_services.py,services/orchestration_service/main.py,services/ui_service/templates/agent_dashboard.html,services/orchestration_service/pipeline_manager.py,test_agent_metadata.py,test_orchestration.py,enhancement1_B_delta_agent_dashboard.md,services/ui_service/templates/base.html,services/ui_service/templates/create.html,services/api_gateway/main.py,services/orchestration_service/agents/__init__.py

# Actively Running Terminals
## Terminal 1 (Active)
### Working Directory: `c:\workspace\ForgeByBob`
### Original command: `python start_all_services.py`
## Terminal 2 (Active)
### Working Directory: `c:\workspace\ForgeByBob`
### Original command: `python start_all_services.py`
## Terminal 3 (Active)
### Working Directory: `c:\workspace\ForgeByBob`
### Original command: `python start_all_services.py`
## Terminal 4 (Active)
### Working Directory: `c:\workspace\ForgeByBob`
### Original command: `python start_all_services.py`
## Terminal 5 (Active)
### Working Directory: `c:\workspace\ForgeByBob`
### Original command: `python start_all_services.py`
## Terminal 6 (Active)
### Working Directory: `c:\workspace\ForgeByBob`
### Original command: `python start_all_services.py`
## Terminal 7 (Active)
### Working Directory: `c:\workspace\ForgeByBob`
### Original command: `python stop_all_services.py; python start_all_services.py`
## Terminal 8 (Active)
### Working Directory: `c:\workspace\ForgeByBob`
### Original command: `python stop_all_services.py; Start-Sleep -Seconds 3; python start_all_services.py`

# Current Time
Current time in ISO 8601 UTC format: 2026-05-02T08:20:05.957Z
User time zone: America/New_York, UTC-4:00

# Current Cost
$0.33

# Review Exclusions
The following file patterns are excluded from code reviews:
- .vscode/**

# Current Mode
<slug>code</slug>
<name>💻 Code</name>
You have not created a todo list yet. Create one with `update_todo_list` if your task is complicated or involves multiple steps.
</environment_details>

---

**Assistant:**

Good! The services are running. I can see the error is still happening - the WriterAgent is also getting a 422 error when trying to create a blog. Let me check the WriterAgent to see what data it's sending:

<read_file>
<args>
<file>
<path>services/orchestration_service/agents/writer_agent.py</path>
</file>
</args>
</read_file>

---

**User:**

[read_file for 'services/orchestration_service/agents/writer_agent.py'. Reading multiple files at once is more efficient for the LLM. If other files are relevant to your current task, please read them simultaneously.] Result:
<files>
<file><path>services/orchestration_service/agents/writer_agent.py</path>
<content lines="1-195">
  1 | """
  2 | Writer Agent - Generates blog content using Granite
  3 | """
  4 | from ..agent_base import BaseAgent, AgentResult
  5 | from services.watsonx_service.granite_client import get_granite_client
  6 | from typing import Dict, Any
  7 | import logging
  8 | import httpx
  9 | from datetime import datetime
 10 | 
 11 | logger = logging.getLogger(__name__)
 12 | 
 13 | # Service URLs
 14 | BLOG_SERVICE_URL = "http://localhost:8001"
 15 | 
 16 | 
 17 | class WriterAgent(BaseAgent):
 18 |     """Agent for generating blog content"""
 19 |     
 20 |     # Agent metadata
 21 |     display_name = "Writer Agent"
 22 |     description = "Generates high-quality blog content using IBM Granite AI. Creates engaging, well-structured articles with proper formatting, headings, and SEO optimization."
 23 |     input_schema = {
 24 |         "prompt": "Blog topic or instructions (required)",
 25 |         "research_brief": "Optional research context",
 26 |         "tone": "Writing tone (default: professional)"
 27 |     }
 28 |     output_schema = {
 29 |         "content": "Generated blog content",
 30 |         "word_count": "Number of words",
 31 |         "char_count": "Number of characters",
 32 |         "model": "AI model used"
 33 |     }
 34 |     
 35 |     def __init__(self, agent_id=None):
 36 |         super().__init__(agent_id)
 37 |         self.granite = get_granite_client()
 38 |         self.system_prompt = """You are a professional blog writer with expertise in
 39 |         creating engaging, well-structured content. Write in a clear, accessible style
 40 |         with proper formatting, headings, and SEO optimization. Always include:
 41 |         - Compelling title
 42 |         - Engaging introduction
 43 |         - Well-structured body with headings
 44 |         - Strong conclusion with call-to-action
 45 |         """
 46 |     
 47 |     async def execute(self, input_data: Dict[str, Any]) -> AgentResult:
 48 |         """
 49 |         Generate blog content and save as draft
 50 |         
 51 |         Expected input_data:
 52 |         {
 53 |             "prompt": "Blog topic or instructions",
 54 |             "research_brief": "Optional research context",
 55 |             "tone": "Optional tone specification"
 56 |         }
 57 |         
 58 |         Returns:
 59 |             AgentResult with generated content and blog draft info
 60 |         """
 61 |         start_time = datetime.utcnow()
 62 |         
 63 |         try:
 64 |             prompt = input_data.get("prompt", "")
 65 |             research_brief = input_data.get("research_brief", "")
 66 |             tone = input_data.get("tone", "professional")
 67 |             
 68 |             if not prompt:
 69 |                 return AgentResult(
 70 |                     success=False,
 71 |                     error="No prompt provided"
 72 |                 )
 73 |             
 74 |             logger.info(f"WriterAgent: Generating content for prompt: {prompt[:50]}...")
 75 |             
 76 |             # Extract title from prompt for blog creation
 77 |             title_parts = prompt.split('\n')[0].strip()
 78 |             title = title_parts[:100] if title_parts else "AI Generated Blog"
 79 |             
 80 |             # Create draft blog via blog service FIRST
 81 |             blog_id = None
 82 |             blog_created = False
 83 |             
 84 |             try:
 85 |                 async with httpx.AsyncClient(timeout=60.0) as client:
 86 |                     # Create blog draft
 87 |                     blog_data = {
 88 |                         "title": title,
 89 |                         "description": f"Generated from prompt: {prompt[:100]}",
 90 |                         "tags": ["ai-generated", "draft"],
 91 |                         "publication_site": "Blog Platform",
 92 |                         "initial_prompt": prompt
 93 |                     }
 94 |                     
 95 |                     logger.info(f"WriterAgent: Creating draft blog via API...")
 96 |                     create_response = await client.post(
 97 |                         f"{BLOG_SERVICE_URL}/blogs",
 98 |                         json=blog_data
 99 |                     )
100 |                     
101 |                     if create_response.status_code == 200:
102 |                         create_result = create_response.json()
103 |                         if create_result.get("success"):
104 |                             blog_id = create_result["data"]["id"]
105 |                             blog_created = True
106 |                             logger.info(f"WriterAgent: Created draft blog {blog_id}")
107 |                             
108 |                             # Now generate content using blog service's generate endpoint
109 |                             # This will properly log the API call to WatsonX logs
110 |                             generate_data = {
111 |                                 "prompt": prompt,
112 |                                 "generation_type": "text"
113 |                             }
114 |                             
115 |                             logger.info(f"WriterAgent: Generating content via blog service API...")
116 |                             generate_response = await client.post(
117 |                                 f"{BLOG_SERVICE_URL}/blogs/{blog_id}/generate",
118 |                                 json=generate_data
119 |                             )
120 |                             
121 |                             if generate_response.status_code == 200:
122 |                                 generate_result = generate_response.json()
123 |                                 if generate_result.get("success"):
124 |                                     content = generate_result["data"]["content"]
125 |                                     version = generate_result["data"]["version"]
126 |                                     logger.info(f"WriterAgent: Generated content (version {version}) for blog {blog_id}")
127 |                                     
128 |                                     # Calculate processing time
129 |                                     end_time = datetime.utcnow()
130 |                                     processing_time_ms = int((end_time - start_time).total_seconds() * 1000)
131 |                                     
132 |                                     result_data = {
133 |                                         "content": content,
134 |                                         "word_count": len(content.split()),
135 |                                         "char_count": len(content),
136 |                                         "model": "ibm/granite-3-8b-instruct",
137 |                                         "processing_time_ms": processing_time_ms,
138 |                                         "blog_id": blog_id,
139 |                                         "blog_status": "draft",
140 |                                         "blog_title": title,
141 |                                         "version": version
142 |                                     }
143 |                                     
144 |                                     return AgentResult(
145 |                                         success=True,
146 |                                         data=result_data,
147 |                                         metadata={
148 |                                             "prompt": prompt,
149 |                                             "tone": tone,
150 |                                             "blog_created": True
151 |                                         }
152 |                                     )
153 |                                 else:
154 |                                     error_msg = generate_result.get("message", "Content generation failed")
155 |                                     logger.error(f"WriterAgent: {error_msg}")
156 |                                     return AgentResult(
157 |                                         success=False,
158 |                                         error=error_msg
159 |                                     )
160 |                             else:
161 |                                 error_msg = f"Blog service returned status {generate_response.status_code}"
162 |                                 logger.error(f"WriterAgent: {error_msg}")
163 |                                 return AgentResult(
164 |                                     success=False,
165 |                                     error=error_msg
166 |                                 )
167 |                     else:
168 |                         error_msg = f"Failed to create blog: {create_response.status_code}"
169 |                         logger.error(f"WriterAgent: {error_msg}")
170 |                         return AgentResult(
171 |                             success=False,
172 |                             error=error_msg
173 |                         )
174 |                         
175 |             except Exception as api_error:
176 |                 logger.error(f"WriterAgent: API call failed: {str(api_error)}")
177 |                 return AgentResult(
178 |                     success=False,
179 |                     error=f"API call failed: {str(api_error)}"
180 |                 )
181 |         
182 |         except Exception as e:
183 |             logger.error(f"WriterAgent: Failed to generate content: {str(e)}")
184 |             return AgentResult(
185 |                 success=False,
186 |                 error=str(e)
187 |             )
188 |         
189 |         # Fallback return (should never reach here)
190 |         return AgentResult(
191 |             success=False,
192 |             error="Unexpected execution path"
193 |         )
194 | 
195 | # Made with Bob
</content>
</file>
</files>
<environment_details>
# VSCode Visible Files
services\ui_service\main.py

# VSCode Open Tabs
.vscode/settings.json,services/ui_service/templates/home.html,.bobalytics.json,.gitignore,services/orchestration_service/agent_base.py,services/orchestration_service/agents/publisher_agent.py,services/orchestration_service/agent_registry.py,services/orchestration_service/agents/writer_agent.py,services/ui_service/main.py,stop_all_services.py,services/orchestration_service/main.py,services/ui_service/templates/agent_dashboard.html,services/orchestration_service/pipeline_manager.py,test_agent_metadata.py,test_orchestration.py,enhancement1_B_delta_agent_dashboard.md,services/ui_service/templates/base.html,services/ui_service/templates/create.html,services/api_gateway/main.py,services/orchestration_service/agents/__init__.py

# Actively Running Terminals
## Terminal 1 (Active)
### Working Directory: `c:\workspace\ForgeByBob`
### Original command: `python start_all_services.py`
## Terminal 2 (Active)
### Working Directory: `c:\workspace\ForgeByBob`
### Original command: `python start_all_services.py`
## Terminal 3 (Active)
### Working Directory: `c:\workspace\ForgeByBob`
### Original command: `python start_all_services.py`
## Terminal 4 (Active)
### Working Directory: `c:\workspace\ForgeByBob`
### Original command: `python start_all_services.py`
## Terminal 5 (Active)
### Working Directory: `c:\workspace\ForgeByBob`
### Original command: `python start_all_services.py`
## Terminal 6 (Active)
### Working Directory: `c:\workspace\ForgeByBob`
### Original command: `python start_all_services.py`
## Terminal 7 (Active)
### Working Directory: `c:\workspace\ForgeByBob`
### Original command: `python stop_all_services.py; python start_all_services.py`
## Terminal 8 (Active)
### Working Directory: `c:\workspace\ForgeByBob`
### Original command: `python stop_all_services.py; Start-Sleep -Seconds 3; python start_all_services.py`

# Current Time
Current time in ISO 8601 UTC format: 2026-05-02T08:20:15.799Z
User time zone: America/New_York, UTC-4:00

# Current Cost
$0.43

# Review Exclusions
The following file patterns are excluded from code reviews:
- .vscode/**

# Current Mode
<slug>code</slug>
<name>💻 Code</name>
You have not created a todo list yet. Create one with `update_todo_list` if your task is complicated or involves multiple steps.
</environment_details>

---

**Assistant:**

I found the issue! In the WriterAgent on line 91, it's sending `"publication_site": "Blog Platform"` which is not a valid enum value. The `PublicationSite` enum only accepts: "medium", "wordpress", "ghost", or "custom". Let me fix this:

<apply_diff>
<path>services/orchestration_service/agents/writer_agent.py</path>
<diff>
<<<<<<< SEARCH
:start_line:87
-------
                    blog_data = {
                        "title": title,
                        "description": f"Generated from prompt: {prompt[:100]}",
                        "tags": ["ai-generated", "draft"],
                        "publication_site": "Blog Platform",
                        "initial_prompt": prompt
                    }
=======
                    blog_data = {
                        "title": title,
                        "description": f"Generated from prompt: {prompt[:100]}",
                        "tags": ["ai-generated", "draft"],
                        "publication_site": None,  # Let it default to None instead of invalid value
                        "initial_prompt": prompt
                    }
>>>>>>> REPLACE
</diff>
</apply_diff>

---

**User:**

[apply_diff for 'services/orchestration_service/agents/writer_agent.py'] Result:
<file_write_result>
<path>services/orchestration_service/agents/writer_agent.py</path>
<operation>modified</operation>
<notice>
<i>You do not need to re-read the file, as you have seen all changes</i>
<i>Proceed with the task using these changes as the new baseline.</i>
</notice>
</file_write_result>

<notice>Making multiple related changes in a single apply_diff is more efficient. If other changes are needed in this file, please include them as additional SEARCH/REPLACE blocks.</notice>
<environment_details>
# VSCode Visible Files
services\orchestration_service\agents\writer_agent.py

# VSCode Open Tabs
.vscode/settings.json,services/ui_service/templates/home.html,.bobalytics.json,.gitignore,services/orchestration_service/agent_base.py,services/orchestration_service/agents/publisher_agent.py,services/orchestration_service/agent_registry.py,services/ui_service/main.py,services/orchestration_service/agents/writer_agent.py,stop_all_services.py,services/orchestration_service/main.py,services/ui_service/templates/agent_dashboard.html,services/orchestration_service/pipeline_manager.py,test_agent_metadata.py,test_orchestration.py,enhancement1_B_delta_agent_dashboard.md,services/ui_service/templates/base.html,services/ui_service/templates/create.html,services/api_gateway/main.py,services/orchestration_service/agents/__init__.py

# Recently Modified Files
These files have been modified since you last accessed them (file was just edited so you may need to re-read it before editing):
services/orchestration_service/agents/writer_agent.py

# Actively Running Terminals
## Terminal 1 (Active)
### Working Directory: `c:\workspace\ForgeByBob`
### Original command: `python start_all_services.py`
## Terminal 2 (Active)
### Working Directory: `c:\workspace\ForgeByBob`
### Original command: `python start_all_services.py`
## Terminal 3 (Active)
### Working Directory: `c:\workspace\ForgeByBob`
### Original command: `python start_all_services.py`
## Terminal 4 (Active)
### Working Directory: `c:\workspace\ForgeByBob`
### Original command: `python start_all_services.py`
## Terminal 5 (Active)
### Working Directory: `c:\workspace\ForgeByBob`
### Original command: `python start_all_services.py`
## Terminal 6 (Active)
### Working Directory: `c:\workspace\ForgeByBob`
### Original command: `python start_all_services.py`
## Terminal 7 (Active)
### Working Directory: `c:\workspace\ForgeByBob`
### Original command: `python stop_all_services.py; python start_all_services.py`
## Terminal 8 (Active)
### Working Directory: `c:\workspace\ForgeByBob`
### Original command: `python stop_all_services.py; Start-Sleep -Seconds 3; python start_all_services.py`

# Current Time
Current time in ISO 8601 UTC format: 2026-05-02T08:20:29.707Z
User time zone: America/New_York, UTC-4:00

# Current Cost
$0.53

# Review Exclusions
The following file patterns are excluded from code reviews:
- .vscode/**

# Current Mode
<slug>code</slug>
<name>💻 Code</name>
You have not created a todo list yet. Create one with `update_todo_list` if your task is complicated or involves multiple steps.
</environment_details>

---

**Assistant:**

Now let me restart the services to apply the fix:

<execute_command>
<command>python stop_all_services.py; Start-Sleep -Seconds 3; python start_all_services.py</command>
</execute_command>

