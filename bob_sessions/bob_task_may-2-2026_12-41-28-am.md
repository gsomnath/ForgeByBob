**User:**

<task>
with the api respinse why the Latest Content not getting populated. can you check that
</task>
<environment_details>
# VSCode Visible Files
requirements.txt

# VSCode Open Tabs
start_all_services.py,requirements.txt,services/blog_service/main.py,.env

# Actively Running Terminals
## Terminal 1 (Active)
### Working Directory: `c:\workspace\ForgeByBob`
### Original command: `Stop-Process -Name python -Force -ErrorAction SilentlyContinue; Start-Sleep -Seconds 2; python start_all_services.py`
## Terminal 2 (Active)
### Working Directory: `c:\workspace\ForgeByBob`
### Original command: `python start_all_services.py`
## Terminal 3 (Active)
### Working Directory: `c:\workspace\ForgeByBob`
### Original command: `Stop-Process -Name python -Force -ErrorAction SilentlyContinue; Start-Sleep -Seconds 2; python start_all_services.py`
## Terminal 4 (Active)
### Working Directory: `c:\workspace\ForgeByBob`
### Original command: `python start_all_services.py`
## Terminal 5 (Active)
### Working Directory: `c:\workspace\ForgeByBob`
### Original command: `Stop-Process -Name python -Force -ErrorAction SilentlyContinue; Start-Sleep -Seconds 3; python start_all_services.py`

# Current Time
Current time in ISO 8601 UTC format: 2026-05-02T04:39:24.331Z
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
enhancement1_B_watsonx_orchestrate_setup.md
enhancement1_C_research_agent.md
enhancement1_D_reviewer_agent_selfcorrection.md
enhancement1_E_realtime_dashboard.md
enhancement2_trust_governance.md
enhancement3_ibm_ace_integration.md
HACKATHON_SERVICES_SETUP.md
IBM_CREDENTIALS_SETUP_GUIDE.md
IMPLEMENTATION_GUIDE.md
pyproject.toml
README.md
requirements.txt
restart_services.bat
SECURITY.md
start_all_services.py
start_services.bat
stop_services.bat
.github/
.vscode/
services/
services/api_gateway/
services/api_gateway/__init__.py
services/api_gateway/main.py
services/blog_service/
services/blog_service/__init__.py
services/blog_service/main.py
services/settings_service/
services/settings_service/__init__.py
services/settings_service/main.py
services/ui_service/
services/ui_service/__init__.py
services/ui_service/main.py
services/ui_service/static/
services/ui_service/templates/
services/ui_service/templates/base.html
services/ui_service/templates/blog_detail.html
services/ui_service/templates/create.html
services/ui_service/templates/gemini_logs.html
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

I'll help you investigate why the Latest Content is not getting populated. Let me start by examining the relevant files to understand the API response and how the Latest Content section is supposed to work.

<read_file>
<args>
<file>
<path>services/ui_service/templates/home.html</path>
</file>
<file>
<path>services/ui_service/main.py</path>
</file>
<file>
<path>services/blog_service/main.py</path>
</file>
</args>
</read_file>

---

**User:**

[read_file for 'services/ui_service/templates/home.html', 'services/ui_service/main.py', 'services/blog_service/main.py'] Result:
<files>
<file><path>services/ui_service/templates/home.html</path>
<content lines="1-46">
 1 | {% extends "base.html" %}
 2 | 
 3 | {% block title %}Blog Writer - Home{% endblock %}
 4 | 
 5 | {% block content %}
 6 | <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 2rem;">
 7 |     <h2>Your Blogs</h2>
 8 |     <a href="/create" class="btn btn-primary">Create New Blog</a>
 9 | </div>
10 | 
11 | {% if blogs %}
12 |     <div class="blog-list">
13 |         {% for blog in blogs %}
14 |         <div class="card blog-card">
15 |             <h3 class="blog-title">{{ blog.title }}</h3>
16 |             <div class="blog-meta">
17 |                 <span class="status status-{{ blog.status }}">{{ blog.status|replace('_', ' ')|title }}</span>
18 |                 <span style="margin-left: 1rem;">Created: {{ blog.created_at[:10] }}</span>
19 |                 {% if blog.current_version > 0 %}
20 |                 <span style="margin-left: 1rem;">Version: {{ blog.current_version }}</span>
21 |                 {% endif %}
22 |             </div>
23 |             {% if blog.description %}
24 |             <p style="margin-bottom: 1rem; color: #666;">{{ blog.description }}</p>
25 |             {% endif %}
26 |             {% if blog.tags %}
27 |             <div style="margin-bottom: 1rem;">
28 |                 {% for tag in blog.tags %}
29 |                 <span style="background: #ecf0f1; padding: 0.25rem 0.5rem; border-radius: 4px; font-size: 0.8rem; margin-right: 0.5rem;">{{ tag }}</span>
30 |                 {% endfor %}
31 |             </div>
32 |             {% endif %}
33 |             <div class="blog-actions">
34 |                 <a href="/blog/{{ blog.id }}" class="btn" style="font-size: 0.9rem; padding: 0.5rem 1rem;">View/Edit</a>
35 |             </div>
36 |         </div>
37 |         {% endfor %}
38 |     </div>
39 | {% else %}
40 |     <div class="card" style="text-align: center; padding: 3rem;">
41 |         <h3 style="color: #666; margin-bottom: 1rem;">No blogs yet</h3>
42 |         <p style="color: #888; margin-bottom: 2rem;">Create your first blog to get started with IBM watsonx.ai powered content generation.</p>
43 |         <a href="/create" class="btn btn-primary">Create Your First Blog</a>
44 |     </div>
45 | {% endif %}
46 | {% endblock %}
</content>
</file>
<file><path>services/ui_service/main.py</path>
<content lines="1-412">
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
 65 | @app.post("/create")
 66 | async def create_blog_submit(
 67 |     request: Request,
 68 |     title: str = Form(...),
 69 |     description: str = Form(""),
 70 |     tags: str = Form(""),
 71 |     publication_site: str = Form(""),
 72 |     initial_prompt: str = Form(...)
 73 | ):
 74 |     """Handle blog creation form submission."""
 75 |     try:
 76 |         # Prepare blog data
 77 |         blog_data = {
 78 |             "title": title,
 79 |             "description": description if description else None,
 80 |             "tags": [tag.strip() for tag in tags.split(",") if tag.strip()],
 81 |             "publication_site": publication_site if publication_site else None,
 82 |             "initial_prompt": initial_prompt
 83 |         }
 84 |         
 85 |         # Create blog via API Gateway
 86 |         async with httpx.AsyncClient() as client:
 87 |             response = await client.post(
 88 |                 f"http://localhost:{settings.api_gateway_port}/api/blogs",
 89 |                 json=blog_data
 90 |             )
 91 |             
 92 |             if response.status_code == 200:
 93 |                 return RedirectResponse(url="/", status_code=303)
 94 |             else:
 95 |                 error_msg = "Failed to create blog"
 96 |                 return templates.TemplateResponse("create.html", {
 97 |                     "request": request,
 98 |                     "error": error_msg
 99 |                 })
100 |     except Exception as e:
101 |         return templates.TemplateResponse("create.html", {
102 |             "request": request,
103 |             "error": str(e)
104 |         })
105 | 
106 | @app.get("/blog/{blog_id}", response_class=HTMLResponse)
107 | async def view_blog(request: Request, blog_id: str):
108 |     """View/edit a specific blog."""
109 |     try:
110 |         # Fetch blog details
111 |         async with httpx.AsyncClient() as client:
112 |             blog_response = await client.get(
113 |                 f"http://localhost:{settings.api_gateway_port}/api/blogs/{blog_id}"
114 |             )
115 |             versions_response = await client.get(
116 |                 f"http://localhost:{settings.api_gateway_port}/api/blogs/{blog_id}/versions"
117 |             )
118 |             comments_response = await client.get(
119 |                 f"http://localhost:{settings.api_gateway_port}/api/blogs/{blog_id}/comments"
120 |             )
121 |             
122 |             blog = None
123 |             versions = []
124 |             comments = []
125 |             
126 |             if blog_response.status_code == 200:
127 |                 blog_data = blog_response.json()
128 |                 blog = blog_data.get("data") if blog_data.get("success") else None
129 |             
130 |             if versions_response.status_code == 200:
131 |                 versions_data = versions_response.json()
132 |                 versions = versions_data.get("data", []) if versions_data.get("success") else []
133 |             
134 |             if comments_response.status_code == 200:
135 |                 comments_data = comments_response.json()
136 |                 comments = comments_data.get("data", []) if comments_data.get("success") else []
137 |             
138 |             if not blog:
139 |                 raise HTTPException(status_code=404, detail="Blog not found")
140 |             
141 |             return templates.TemplateResponse("blog_detail.html", {
142 |                 "request": request,
143 |                 "blog": blog,
144 |                 "versions": versions,
145 |                 "comments": comments
146 |             })
147 |     except HTTPException:
148 |         raise
149 |     except Exception as e:
150 |         raise HTTPException(status_code=500, detail=str(e))
151 | 
152 | @app.post("/blog/{blog_id}/generate")
153 | async def generate_content(
154 |     request: Request,
155 |     blog_id: str,
156 |     prompt: str = Form(...),
157 |     generation_type: str = Form("all")  # Default to "all" for backward compatibility
158 | ):
159 |     """Generate new content for a blog."""
160 |     try:
161 |         async with httpx.AsyncClient() as client:
162 |             response = await client.post(
163 |                 f"http://localhost:{settings.api_gateway_port}/api/blogs/{blog_id}/generate",
164 |                 json={"prompt": prompt, "generation_type": generation_type}
165 |             )
166 |             
167 |             if response.status_code == 200:
168 |                 return RedirectResponse(url=f"/blog/{blog_id}", status_code=303)
169 |             else:
170 |                 # Try to get detailed error from response
171 |                 try:
172 |                     error_data = response.json()
173 |                     error_msg = error_data.get("detail", "Failed to generate content")
174 |                 except:
175 |                     error_msg = f"Failed to generate content (HTTP {response.status_code})"
176 |                 return RedirectResponse(url=f"/blog/{blog_id}?error={error_msg}", status_code=303)
177 |     except Exception as e:
178 |         return RedirectResponse(url=f"/blog/{blog_id}?error={str(e)}", status_code=303)
179 | 
180 | @app.post("/blog/{blog_id}/comment")
181 | async def add_comment(
182 |     request: Request,
183 |     blog_id: str,
184 |     content: str = Form(...),
185 |     requested_changes: str = Form("")
186 | ):
187 |     """Add a comment to a blog."""
188 |     try:
189 |         comment_data = {
190 |             "content": content,
191 |             "requested_changes": requested_changes if requested_changes else None
192 |         }
193 |         
194 |         async with httpx.AsyncClient() as client:
195 |             response = await client.post(
196 |                 f"http://localhost:{settings.api_gateway_port}/api/blogs/{blog_id}/comments",
197 |                 json=comment_data
198 |             )
199 |             
200 |             return RedirectResponse(url=f"/blog/{blog_id}", status_code=303)
201 |     except Exception as e:
202 |         return RedirectResponse(url=f"/blog/{blog_id}?error={str(e)}", status_code=303)
203 | 
204 | @app.get("/api/blogs/{blog_id}/versions/{version_num}/content")
205 | async def get_blog_version_content(blog_id: str, version_num: int):
206 |     """Proxy request to get blog version content."""
207 |     try:
208 |         async with httpx.AsyncClient() as client:
209 |             response = await client.get(
210 |                 f"http://localhost:{settings.api_gateway_port}/api/blogs/{blog_id}/versions/{version_num}/content"
211 |             )
212 |             
213 |             if response.status_code == 200:
214 |                 return response.json()
215 |             else:
216 |                 return {"success": False, "message": "Failed to load content"}
217 |     except Exception as e:
218 |         return {"success": False, "message": f"Error: {str(e)}"}
219 | 
220 | @app.put("/api/blogs/{blog_id}/content")
221 | async def update_blog_content(blog_id: str, content_data: dict):
222 |     """Proxy request to update blog content."""
223 |     try:
224 |         async with httpx.AsyncClient() as client:
225 |             response = await client.put(
226 |                 f"http://localhost:{settings.api_gateway_port}/api/blogs/{blog_id}/content",
227 |                 json=content_data
228 |             )
229 |             
230 |             if response.status_code == 200:
231 |                 return response.json()
232 |             else:
233 |                 return {"success": False, "message": "Failed to update content"}
234 |     except Exception as e:
235 |         return {"success": False, "message": f"Error: {str(e)}"}
236 | 
237 | @app.post("/blog/{blog_id}/content")
238 | async def save_blog_content(
239 |     request: Request,
240 |     blog_id: str,
241 |     content: str = Form(...)
242 | ):
243 |     """Save manually edited blog content."""
244 |     try:
245 |         async with httpx.AsyncClient() as client:
246 |             response = await client.put(
247 |                 f"http://localhost:{settings.api_gateway_port}/api/blogs/{blog_id}/content",
248 |                 json={"content": content}
249 |             )
250 |             
251 |             if response.status_code == 200:
252 |                 return RedirectResponse(url=f"/blog/{blog_id}?success=Content saved successfully", status_code=303)
253 |             else:
254 |                 error_msg = "Failed to save content"
255 |                 return RedirectResponse(url=f"/blog/{blog_id}?error={error_msg}", status_code=303)
256 |     except Exception as e:
257 |         return RedirectResponse(url=f"/blog/{blog_id}?error={str(e)}", status_code=303)
258 | 
259 | @app.post("/blog/{blog_id}/versions/{version_num}/delete")
260 | async def delete_blog_version(
261 |     request: Request,
262 |     blog_id: str,
263 |     version_num: int
264 | ):
265 |     """Delete a specific blog version."""
266 |     try:
267 |         async with httpx.AsyncClient() as client:
268 |             response = await client.delete(
269 |                 f"http://localhost:{settings.api_gateway_port}/api/blogs/{blog_id}/versions/{version_num}"
270 |             )
271 |             
272 |             if response.status_code == 200:
273 |                 return RedirectResponse(url=f"/blog/{blog_id}?success=Version {version_num} deleted successfully", status_code=303)
274 |             else:
275 |                 data = response.json() if response.headers.get("content-type", "").startswith("application/json") else {}
276 |                 error_msg = data.get("detail", "Failed to delete version")
277 |                 return RedirectResponse(url=f"/blog/{blog_id}?error={error_msg}", status_code=303)
278 |     except Exception as e:
279 |         return RedirectResponse(url=f"/blog/{blog_id}?error={str(e)}", status_code=303)
280 | 
281 | @app.get("/settings", response_class=HTMLResponse)
282 | async def settings_page(request: Request):
283 |     """Settings page."""
284 |     try:
285 |         # Fetch current settings
286 |         async with httpx.AsyncClient() as client:
287 |             response = await client.get(
288 |                 f"http://localhost:{settings.settings_service_port}/settings"
289 |             )
290 |             
291 |             current_settings = {}
292 |             if response.status_code == 200:
293 |                 settings_data = response.json()
294 |                 current_settings = settings_data.get("data", {}) if settings_data.get("success") else {}
295 |             
296 |             return templates.TemplateResponse("settings.html", {
297 |                 "request": request,
298 |                 "settings": current_settings
299 |             })
300 |     except Exception as e:
301 |         return templates.TemplateResponse("settings.html", {
302 |             "request": request,
303 |             "error": str(e),
304 |             "settings": {}
305 |         })
306 | 
307 | @app.post("/settings")
308 | async def update_settings(
309 |     request: Request,
310 |     ibm_cloud_api_key: str = Form(""),
311 |     watsonx_project_id: str = Form(""),
312 |     watsonx_url: str = Form("https://us-south.ml.cloud.ibm.com"),
313 |     watsonx_model_id: str = Form("meta-llama/llama-3-3-70b-instruct"),
314 |     source_folder: str = Form(""),
315 |     default_publication_site: str = Form("")
316 | ):
317 |     """Update settings."""
318 |     try:
319 |         settings_data = {}
320 |         
321 |         if ibm_cloud_api_key:
322 |             settings_data["ibm_cloud_api_key"] = ibm_cloud_api_key
323 |         if watsonx_project_id:
324 |             settings_data["watsonx_project_id"] = watsonx_project_id
325 |         if watsonx_url:
326 |             settings_data["watsonx_url"] = watsonx_url
327 |         if watsonx_model_id:
328 |             settings_data["watsonx_model_id"] = watsonx_model_id
329 |         if source_folder:
330 |             settings_data["source_folder"] = source_folder
331 |         if default_publication_site:
332 |             settings_data["default_publication_site"] = default_publication_site
333 |         
334 |         async with httpx.AsyncClient() as client:
335 |             response = await client.put(
336 |                 f"http://localhost:{settings.settings_service_port}/settings",
337 |                 json=settings_data
338 |             )
339 |             
340 |             if response.status_code == 200:
341 |                 return RedirectResponse(url="/settings?success=1", status_code=303)
342 |             else:
343 |                 return RedirectResponse(url="/settings?error=Failed to update settings", status_code=303)
344 |     except Exception as e:
345 |         return RedirectResponse(url=f"/settings?error={str(e)}", status_code=303)
346 | 
347 | @app.get("/watsonx-logs", response_class=HTMLResponse)
348 | async def watsonx_logs_page(request: Request, page: int = 1):
349 |     """WatsonX API logs page with pagination."""
350 |     try:
351 |         # Fetch WatsonX logs from blog service
352 |         async with httpx.AsyncClient() as client:
353 |             response = await client.get(
354 |                 f"http://localhost:{settings.blog_service_port}/watsonx-logs?page={page}&page_size=10"
355 |             )
356 |             
357 |             logs_data = []
358 |             pagination = {}
359 |             
360 |             if response.status_code == 200:
361 |                 data = response.json()
362 |                 if data.get("success"):
363 |                     logs_data = data.get("data", {}).get("logs", [])
364 |                     pagination = data.get("data", {}).get("pagination", {})
365 |             
366 |             return templates.TemplateResponse("watsonx_logs.html", {
367 |                 "request": request,
368 |                 "logs": logs_data,
369 |                 "pagination": pagination
370 |             })
371 |     except Exception as e:
372 |         return templates.TemplateResponse("watsonx_logs.html", {
373 |             "request": request,
374 |             "error": str(e),
375 |             "logs": [],
376 |             "pagination": {}
377 |         })
378 | 
379 | # Keep old endpoint for backward compatibility
380 | @app.get("/gemini-logs", response_class=HTMLResponse)
381 | async def gemini_logs_compat(request: Request, page: int = 1):
382 |     """WatsonX API logs (compatibility endpoint)."""
383 |     return await watsonx_logs_page(request, page)
384 | 
385 | @app.get("/imagen-logs", response_class=HTMLResponse)
386 | async def imagen_logs_page(request: Request, page: int = 1):
387 |     """Image generation logs page (deprecated feature)."""
388 |     try:
389 |         # Return empty page as feature is deprecated
390 |         return templates.TemplateResponse("imagen_logs.html", {
391 |             "request": request,
392 |             "logs": [],
393 |             "pagination": {
394 |                 "current_page": 1,
395 |                 "page_size": 10,
396 |                 "total_logs": 0,
397 |                 "total_pages": 0,
398 |                 "has_next": False,
399 |                 "has_prev": False
400 |             }
401 |         })
402 |     except Exception as e:
403 |         return templates.TemplateResponse("imagen_logs.html", {
404 |             "request": request,
405 |             "error": str(e),
406 |             "logs": [],
407 |             "pagination": {}
408 |         })
409 | 
410 | if __name__ == "__main__":
411 |     import uvicorn
412 |     uvicorn.run(app, host="0.0.0.0", port=settings.ui_service_port)
</content>
</file>
<file><path>services/blog_service/main.py</path>
<content lines="1-857">
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
 12 | from datetime import datetime, timezone
 13 | 
 14 | # Add the project root to the Python path
 15 | project_root = Path(__file__).parent.parent.parent
 16 | sys.path.append(str(project_root))
 17 | 
 18 | from shared.config import settings
 19 | from shared.models import (
 20 |     Blog, BlogCreate, BlogUpdate, BlogVersion, Comment, CommentCreate,
 21 |     APIResponse, BlogStatus, WatsonxAPILog
 22 | )
 23 | from shared.utils import (
 24 |     generate_id, get_current_timestamp, create_blog_folder_structure, save_blog_version,
 25 |     save_prompt, get_next_version_number, list_blog_versions,
 26 |     read_file_content, ensure_directory_exists
 27 | )
 28 | 
 29 | # Import IBM watsonx client
 30 | from services.watsonx_service.granite_client import get_granite_client
 31 | 
 32 | # Image generation will use placeholder images
 33 | IMAGEN_AVAILABLE = False
 34 | 
 35 | @asynccontextmanager
 36 | async def lifespan(app: FastAPI):
 37 |     """Manage application lifecycle."""
 38 |     ensure_directory_exists(settings.source_folder)
 39 |     ensure_data_directory()
 40 |     load_blogs_from_file()
 41 |     load_comments_from_file()
 42 |     load_watsonx_logs_from_file()
 43 |     yield
 44 | 
 45 | 
 46 | app = FastAPI(
 47 |     title="Blog Service",
 48 |     description="Microservice for blog content management and AI generation",
 49 |     version="1.0.0",
 50 |     lifespan=lifespan
 51 | )
 52 | 
 53 | # IBM watsonx client (initialized globally)
 54 | watsonx_client = None
 55 | 
 56 | async def get_watsonx_client():
 57 |     """Get or initialize IBM watsonx client."""
 58 |     global watsonx_client
 59 |     if watsonx_client is None:
 60 |         watsonx_client = get_granite_client()
 61 |     return watsonx_client
 62 | 
 63 | async def get_current_settings():
 64 |     """Get all current settings from settings service."""
 65 |     try:
 66 |         async with httpx.AsyncClient() as client:
 67 |             response = await client.get(f"{settings.settings_service_url}/settings/raw", timeout=5.0)
 68 |             if response.status_code == 200:
 69 |                 data = response.json()
 70 |                 if data.get("success") and data.get("data"):
 71 |                     return data["data"]
 72 |     except Exception as e:
 73 |         print(f"Warning: Settings service exception: {e}")
 74 |     return None
 75 | 
 76 | 
 77 | async def generate_image_prompts_with_watsonx(content: str, blog_title: str, user_prompt: str = "") -> List[str]:
 78 |     """Use IBM watsonx.ai to generate high-quality image prompts based on blog content."""
 79 |     try:
 80 |         # Get watsonx client
 81 |         client = await get_watsonx_client()
 82 |         if not client:
 83 |             # Fallback to default prompts
 84 |             return [
 85 |                 f"Professional illustration related to {blog_title}, clean modern style, high quality, detailed artwork",
 86 |                 f"Abstract representation of {blog_title} concept, minimalist design, professional quality"
 87 |             ]
 88 |         
 89 |         # Include user prompt if provided
 90 |         user_prompt_context = ""
 91 |         if user_prompt:
 92 |             user_prompt_context = f"""
 93 | 
 94 | Additional User Requirements for Images: {user_prompt}
 95 | Please incorporate these requirements into the image prompts where relevant.
 96 | """
 97 |         
 98 |         # Create a prompt for watsonx to generate image descriptions
 99 |         watsonx_prompt = f"""
100 | Based on this blog post title and content, create 2 detailed, high-quality image generation prompts that would create visually appealing images to accompany the article.
101 | 
102 | Blog Title: {blog_title}
103 | 
104 | Blog Content Excerpt: {content[:1000]}...{user_prompt_context}
105 | 
106 | Requirements for each image prompt:
107 | - Professional, high-quality visual style
108 | - Relevant to the blog content themes
109 | - Descriptive enough for AI image generation
110 | - Avoid text/words in images
111 | - Modern, clean aesthetic
112 | - Each prompt should be different and complementary
113 | 
114 | Please provide exactly 2 image prompts, each on a separate line, starting with "Image 1:" and "Image 2:"
115 | """
116 | 
117 |         # Generate prompts using IBM watsonx
118 |         response = client.generate(watsonx_prompt, max_tokens=500)
119 |         generated_text = response.strip()
120 |         
121 |         # Parse the generated prompts
122 |         image_prompts = []
123 |         lines = generated_text.split('\n')
124 |         
125 |         for line in lines:
126 |             line = line.strip()
127 |             if line.startswith("Image 1:"):
128 |                 image_prompts.append(line.replace("Image 1:", "").strip())
129 |             elif line.startswith("Image 2:"):
130 |                 image_prompts.append(line.replace("Image 2:", "").strip())
131 |         
132 |         # Ensure we have exactly 2 prompts
133 |         if len(image_prompts) < 2:
134 |             # Fallback if parsing failed
135 |             image_prompts = [
136 |                 f"Professional illustration related to {blog_title}, clean modern style, high quality, detailed artwork",
137 |                 f"Abstract representation of {blog_title} concept, minimalist design, professional quality"
138 |             ]
139 |         
140 |         return image_prompts[:2]  # Ensure exactly 2 prompts
141 |         
142 |     except Exception as e:
143 |         print(f"Error generating image prompts with IBM watsonx: {e}")
144 |         # Fallback to default prompts
145 |         return [
146 |             f"Professional illustration related to {blog_title}, clean modern style, high quality, detailed artwork",
147 |             f"Abstract representation of {blog_title} concept, minimalist design, professional quality"
148 |         ]
149 | 
150 | def generate_static_image_url(blog_id: str, image_number: int) -> str:
151 |     """Generate a static image URL that won't change on page refresh."""
152 |     seed = f"{blog_id}_{image_number}"
153 |     hash_value = hashlib.md5(seed.encode()).hexdigest()
154 |     image_id = int(hash_value[:6], 16) % 1000 + 1
155 |     return f"https://picsum.photos/id/{image_id}/800/600"
156 | 
157 | def save_imagen_response_to_file(imagen_response, blog_id: str, image_number: int) -> str:
158 |     """Save Imagen API response image to local file and return the URL."""
159 |     try:
160 |         # Create images directory if it doesn't exist
161 |         images_dir = Path("generated_images")
162 |         images_dir.mkdir(exist_ok=True)
163 |         
164 |         # Create filename with blog_id and image number
165 |         filename = f"{blog_id}_image_{image_number}_{uuid.uuid4().hex[:8]}.png"
166 |         file_path = images_dir / filename
167 |         
168 |         # Get the first image from the response
169 |         if imagen_response.images and len(imagen_response.images) > 0:
170 |             image = imagen_response.images[0]
171 |             
172 |             # Save the image to file
173 |             with open(file_path, "wb") as f:
174 |                 f.write(image._image_bytes)
175 |             
176 |             # Return local URL that will be served by UI service
177 |             return f"http://localhost:8003/images/{filename}"
178 |         
179 |         return None
180 |     except Exception as e:
181 |         print(f"Error saving Imagen response to file: {e}")
182 |         return None
183 | 
184 | async def generate_images_with_placeholder(content: str, blog_title: str, blog_id: str, user_prompt: str = "") -> List[str]:
185 |     """Image generation is disabled. Returns empty list."""
186 |     # Image generation functionality has been disabled
187 |     return []
188 | 
189 | # Persistent storage paths
190 | DATA_DIR = Path("data")
191 | BLOGS_DB_FILE = DATA_DIR / "blogs.json"
192 | COMMENTS_DB_FILE = DATA_DIR / "comments.json"
193 | WATSONX_LOGS_FILE = DATA_DIR / "watsonx_logs.json"
194 | 
195 | # In-memory storage (loaded from persistent storage)
196 | blogs_db = {}
197 | comments_db = {}
198 | watsonx_logs = []  # List to store API logs, ordered by timestamp
199 | 
200 | def ensure_data_directory():
201 |     """Ensure data directory exists."""
202 |     DATA_DIR.mkdir(exist_ok=True)
203 | 
204 | def load_blogs_from_file():
205 |     """Load blogs from persistent storage."""
206 |     global blogs_db
207 |     try:
208 |         if BLOGS_DB_FILE.exists():
209 |             with open(BLOGS_DB_FILE, 'r', encoding='utf-8') as f:
210 |                 data = json.load(f)
211 |                 # Convert back to Blog objects
212 |                 for blog_id, blog_data in data.items():
213 |                     # Convert datetime strings back to datetime objects
214 |                     if 'created_at' in blog_data:
215 |                         blog_data['created_at'] = datetime.fromisoformat(blog_data['created_at'].replace('Z', '+00:00'))
216 |                     if 'updated_at' in blog_data:
217 |                         blog_data['updated_at'] = datetime.fromisoformat(blog_data['updated_at'].replace('Z', '+00:00'))
218 |                     blogs_db[blog_id] = Blog(**blog_data)
219 |                 print(f"Loaded {len(blogs_db)} blogs from persistent storage")
220 |     except Exception as e:
221 |         print(f"Error loading blogs from file: {e}")
222 |         blogs_db = {}
223 | 
224 | def save_blogs_to_file():
225 |     """Save blogs to persistent storage."""
226 |     try:
227 |         ensure_data_directory()
228 |         # Convert Blog objects to serializable dict
229 |         data = {}
230 |         for blog_id, blog in blogs_db.items():
231 |             blog_dict = blog.model_dump(mode='json')
232 |             data[blog_id] = blog_dict
233 |         
234 |         with open(BLOGS_DB_FILE, 'w', encoding='utf-8') as f:
235 |             json.dump(data, f, indent=2, ensure_ascii=False)
236 |     except Exception as e:
237 |         print(f"Error saving blogs to file: {e}")
238 | 
239 | def load_comments_from_file():
240 |     """Load comments from persistent storage."""
241 |     global comments_db
242 |     try:
243 |         if COMMENTS_DB_FILE.exists():
244 |             with open(COMMENTS_DB_FILE, 'r', encoding='utf-8') as f:
245 |                 data = json.load(f)
246 |                 # Convert back to Comment objects
247 |                 for blog_id, comments_list in data.items():
248 |                     comments_db[blog_id] = []
249 |                     for comment_data in comments_list:
250 |                         # Convert datetime strings back to datetime objects
251 |                         if 'created_at' in comment_data:
252 |                             comment_data['created_at'] = datetime.fromisoformat(comment_data['created_at'].replace('Z', '+00:00'))
253 |                         comments_db[blog_id].append(Comment(**comment_data))
254 |                 print(f"Loaded comments for {len(comments_db)} blogs from persistent storage")
255 |     except Exception as e:
256 |         print(f"Error loading comments from file: {e}")
257 |         comments_db = {}
258 | 
259 | def save_comments_to_file():
260 |     """Save comments to persistent storage."""
261 |     try:
262 |         ensure_data_directory()
263 |         # Convert Comment objects to serializable dict
264 |         data = {}
265 |         for blog_id, comments_list in comments_db.items():
266 |             data[blog_id] = [comment.model_dump(mode='json') for comment in comments_list]
267 |         
268 |         with open(COMMENTS_DB_FILE, 'w', encoding='utf-8') as f:
269 |             json.dump(data, f, indent=2, ensure_ascii=False)
270 |     except Exception as e:
271 |         print(f"Error saving comments to file: {e}")
272 | 
273 | def load_watsonx_logs_from_file():
274 |     """Load WatsonX API logs from persistent storage."""
275 |     global watsonx_logs
276 |     try:
277 |         if WATSONX_LOGS_FILE.exists():
278 |             with open(WATSONX_LOGS_FILE, 'r', encoding='utf-8') as f:
279 |                 data = json.load(f)
280 |                 watsonx_logs = []
281 |                 for log_data in data:
282 |                     # Convert datetime strings back to datetime objects
283 |                     if 'request_timestamp' in log_data:
284 |                         log_data['request_timestamp'] = datetime.fromisoformat(log_data['request_timestamp'].replace('Z', '+00:00'))
285 |                     if 'response_timestamp' in log_data and log_data['response_timestamp']:
286 |                         log_data['response_timestamp'] = datetime.fromisoformat(log_data['response_timestamp'].replace('Z', '+00:00'))
287 |                     watsonx_logs.append(WatsonxAPILog(**log_data))
288 |                 # Sort by timestamp (newest first)
289 |                 watsonx_logs.sort(key=lambda x: x.request_timestamp, reverse=True)
290 |                 # Keep only last 200 logs
291 |                 watsonx_logs = watsonx_logs[:200]
292 |                 print(f"Loaded {len(watsonx_logs)} WatsonX API logs from persistent storage")
293 |     except Exception as e:
294 |         print(f"Error loading WatsonX logs from file: {e}")
295 |         watsonx_logs = []
296 | 
297 | def save_watsonx_logs_to_file():
298 |     """Save WatsonX API logs to persistent storage."""
299 |     try:
300 |         ensure_data_directory()
301 |         # Keep only last 200 logs
302 |         logs_to_save = watsonx_logs[:200]
303 |         # Convert to serializable dict
304 |         data = [log.model_dump(mode='json') for log in logs_to_save]
305 |         
306 |         with open(WATSONX_LOGS_FILE, 'w', encoding='utf-8') as f:
307 |             json.dump(data, f, indent=2, ensure_ascii=False)
308 |     except Exception as e:
309 |         print(f"Error saving WatsonX logs to file: {e}")
310 | 
311 | def log_watsonx_request(blog_id: str, prompt: str, model_used: str = "ibm/granite-4-h-small"):
312 |     """Log a WatsonX API request."""
313 |     global watsonx_logs
314 |     log_entry = WatsonxAPILog(
315 |         id=generate_id(),
316 |         request_timestamp=get_current_timestamp(),
317 |         blog_id=blog_id,
318 |         prompt=prompt,
319 |         model_used=model_used,
320 |         success=False  # Will be updated when response is received
321 |     )
322 |     watsonx_logs.insert(0, log_entry)  # Add to beginning (newest first)
323 |     return log_entry.id
324 | 
325 | def log_watsonx_response(log_id: str, response_content: str = None, error_message: str = None, processing_time_ms: int = None):
326 |     """Update a WatsonX API log with response information."""
327 |     global watsonx_logs
328 |     for log_entry in watsonx_logs:
329 |         if log_entry.id == log_id:
330 |             log_entry.response_timestamp = get_current_timestamp()
331 |             log_entry.response_content = response_content
332 |             log_entry.error_message = error_message
333 |             log_entry.processing_time_ms = processing_time_ms
334 |             log_entry.success = response_content is not None
335 |             break
336 |     
337 |     # Keep only last 200 logs
338 |     watsonx_logs = watsonx_logs[:200]
339 |     save_watsonx_logs_to_file()
340 | 
341 | 
342 | @app.get("/")
343 | async def root():
344 |     """Root endpoint."""
345 |     return APIResponse(
346 |         success=True,
347 |         message="Blog Service is running",
348 |         data={"version": "1.0.0"}
349 |     )
350 | 
351 | @app.get("/health")
352 | async def health_check():
353 |     """Health check endpoint."""
354 |     return {"status": "healthy", "service": "blog-service"}
355 | 
356 | @app.get("/watsonx-logs", response_model=APIResponse)
357 | async def get_watsonx_logs(page: int = 1, page_size: int = 10):
358 |     """Get WatsonX API logs with pagination."""
359 |     try:
360 |         # Calculate pagination
361 |         total_logs = len(watsonx_logs)
362 |         start_idx = (page - 1) * page_size
363 |         end_idx = start_idx + page_size
364 |         
365 |         # Get logs for current page
366 |         page_logs = watsonx_logs[start_idx:end_idx]
367 |         logs_data = [log.model_dump(mode='json') for log in page_logs]
368 |         
369 |         # Calculate pagination info
370 |         total_pages = (total_logs + page_size - 1) // page_size
371 |         
372 |         return APIResponse(
373 |             success=True,
374 |             message="WatsonX logs retrieved successfully",
375 |             data={
376 |                 "logs": logs_data,
377 |                 "pagination": {
378 |                     "current_page": page,
379 |                     "page_size": page_size,
380 |                     "total_logs": total_logs,
381 |                     "total_pages": total_pages,
382 |                     "has_next": page < total_pages,
383 |                     "has_prev": page > 1
384 |                 }
385 |             }
386 |         )
387 |     except Exception as e:
388 |         raise HTTPException(status_code=500, detail=str(e))
389 | 
390 | # Keep old endpoint for backward compatibility
391 | @app.get("/gemini-logs", response_model=APIResponse)
392 | async def get_gemini_logs_compat(page: int = 1, page_size: int = 10):
393 |     """Get WatsonX API logs (compatibility endpoint)."""
394 |     return await get_watsonx_logs(page, page_size)
395 | 
396 | @app.get("/imagen-logs", response_model=APIResponse)
397 | async def get_imagen_logs(page: int = 1, page_size: int = 10):
398 |     """Get image generation logs (placeholder - no longer used)."""
399 |     try:
400 |         # Return empty logs as image generation is no longer active
401 |         return APIResponse(
402 |             success=True,
403 |             message="Image generation logs (feature deprecated)",
404 |             data={
405 |                 "logs": [],
406 |                 "pagination": {
407 |                     "current_page": page,
408 |                     "page_size": page_size,
409 |                     "total_logs": 0,
410 |                     "total_pages": 0,
411 |                     "has_next": False,
412 |                     "has_prev": False
413 |                 }
414 |             }
415 |         )
416 |     except Exception as e:
417 |         raise HTTPException(status_code=500, detail=str(e))
418 |         
419 | 
420 | @app.post("/blogs", response_model=APIResponse)
421 | async def create_blog(blog_data: BlogCreate):
422 |     """Create a new blog."""
423 |     try:
424 |         blog_id = generate_id()
425 |         
426 |         # Create folder structure
427 |         folder_path = create_blog_folder_structure(settings.source_folder, blog_data.title)
428 |         
429 |         # Save initial prompt
430 |         save_prompt(folder_path, blog_data.initial_prompt, "initial_prompt.txt")
431 |         
432 |         # Create blog record
433 |         blog = Blog(
434 |             id=blog_id,
435 |             title=blog_data.title,
436 |             description=blog_data.description,
437 |             tags=blog_data.tags,
438 |             publication_site=blog_data.publication_site,
439 |             status=BlogStatus.DRAFT,
440 |             created_at=get_current_timestamp(),
441 |             updated_at=get_current_timestamp(),
442 |             folder_path=folder_path,
443 |             current_version=0
444 |         )
445 |         
446 |         blogs_db[blog_id] = blog
447 |         save_blogs_to_file()  # Save to persistent storage
448 |         
449 |         return APIResponse(
450 |             success=True,
451 |             message="Blog created successfully",
452 |             data=blog.model_dump(mode='json')
453 |         )
454 |     except Exception as e:
455 |         raise HTTPException(status_code=500, detail=str(e))
456 | 
457 | @app.get("/blogs", response_model=APIResponse)
458 | async def get_blogs():
459 |     """Get all blogs."""
460 |     try:
461 |         blogs_list = [blog.model_dump(mode='json') for blog in blogs_db.values()]
462 |         return APIResponse(
463 |             success=True,
464 |             message="Blogs retrieved successfully",
465 |             data=blogs_list
466 |         )
467 |     except Exception as e:
468 |         raise HTTPException(status_code=500, detail=str(e))
469 | 
470 | @app.get("/blogs/{blog_id}", response_model=APIResponse)
471 | async def get_blog(blog_id: str):
472 |     """Get a specific blog."""
473 |     try:
474 |         if blog_id not in blogs_db:
475 |             raise HTTPException(status_code=404, detail="Blog not found")
476 |         
477 |         blog = blogs_db[blog_id]
478 |         return APIResponse(
479 |             success=True,
480 |             message="Blog retrieved successfully",
481 |             data=blog.model_dump(mode='json')
482 |         )
483 |     except HTTPException:
484 |         raise
485 |     except Exception as e:
486 |         raise HTTPException(status_code=500, detail=str(e))
487 | 
488 | @app.put("/blogs/{blog_id}", response_model=APIResponse)
489 | async def update_blog(blog_id: str, blog_update: BlogUpdate):
490 |     """Update a blog."""
491 |     try:
492 |         if blog_id not in blogs_db:
493 |             raise HTTPException(status_code=404, detail="Blog not found")
494 |         
495 |         blog = blogs_db[blog_id]
496 |         
497 |         # Update fields
498 |         if blog_update.title is not None:
499 |             blog.title = blog_update.title
500 |         if blog_update.description is not None:
501 |             blog.description = blog_update.description
502 |         if blog_update.tags is not None:
503 |             blog.tags = blog_update.tags
504 |         if blog_update.publication_site is not None:
505 |             blog.publication_site = blog_update.publication_site
506 |         if blog_update.status is not None:
507 |             blog.status = blog_update.status
508 |         
509 |         blog.updated_at = get_current_timestamp()
510 |         save_blogs_to_file()  # Save to persistent storage
511 |         
512 |         return APIResponse(
513 |             success=True,
514 |             message="Blog updated successfully",
515 |             data=blog.model_dump(mode='json')
516 |         )
517 |     except HTTPException:
518 |         raise
519 |     except Exception as e:
520 |         raise HTTPException(status_code=500, detail=str(e))
521 | 
522 | @app.delete("/blogs/{blog_id}", response_model=APIResponse)
523 | async def delete_blog(blog_id: str):
524 |     """Delete a blog."""
525 |     try:
526 |         if blog_id not in blogs_db:
527 |             raise HTTPException(status_code=404, detail="Blog not found")
528 |         
529 |         del blogs_db[blog_id]
530 |         save_blogs_to_file()  # Save to persistent storage
531 |         
532 |         return APIResponse(
533 |             success=True,
534 |             message="Blog deleted successfully"
535 |         )
536 |     except HTTPException:
537 |         raise
538 |     except Exception as e:
539 |         raise HTTPException(status_code=500, detail=str(e))
540 | 
541 | @app.get("/blogs/{blog_id}/versions", response_model=APIResponse)
542 | async def get_blog_versions(blog_id: str):
543 |     """Get all versions of a blog."""
544 |     try:
545 |         if blog_id not in blogs_db:
546 |             raise HTTPException(status_code=404, detail="Blog not found")
547 |         
548 |         blog = blogs_db[blog_id]
549 |         versions = list_blog_versions(blog.folder_path)
550 |         
551 |         return APIResponse(
552 |             success=True,
553 |             message="Blog versions retrieved successfully",
554 |             data=versions
555 |         )
556 |     except HTTPException:
557 |         raise
558 |     except Exception as e:
559 |         raise HTTPException(status_code=500, detail=str(e))
560 | 
561 | @app.get("/blogs/{blog_id}/versions/{version_num}/content", response_model=APIResponse)
562 | async def get_blog_version_content(blog_id: str, version_num: int):
563 |     """Get the content of a specific blog version."""
564 |     try:
565 |         if blog_id not in blogs_db:
566 |             raise HTTPException(status_code=404, detail="Blog not found")
567 |         
568 |         blog = blogs_db[blog_id]
569 |         final_folder = Path(blog.folder_path) / "final"
570 |         version_file = final_folder / f"v{version_num}.md"
571 |         
572 |         if not version_file.exists():
573 |             raise HTTPException(status_code=404, detail="Version not found")
574 |         
575 |         with open(version_file, 'r', encoding='utf-8') as f:
576 |             content = f.read()
577 |         
578 |         return APIResponse(
579 |             success=True,
580 |             message="Version content retrieved successfully",
581 |             data={"content": content}
582 |         )
583 |     except HTTPException:
584 |         raise
585 |     except Exception as e:
586 |         raise HTTPException(status_code=500, detail=str(e))
587 | 
588 | @app.put("/blogs/{blog_id}/content", response_model=APIResponse)
589 | async def update_blog_content(blog_id: str, content_data: dict):
590 |     """Update blog content manually."""
591 |     try:
592 |         if blog_id not in blogs_db:
593 |             raise HTTPException(status_code=404, detail="Blog not found")
594 |         
595 |         blog = blogs_db[blog_id]
596 |         new_content = content_data.get("content", "")
597 |         
598 |         if not new_content.strip():
599 |             raise HTTPException(status_code=400, detail="Content cannot be empty")
600 |         
601 |         # Save as new version if this is different from current content
602 |         if blog.latest_content != new_content:
603 |             # Get next version number and save content
604 |             version_number = get_next_version_number(blog.folder_path)
605 |             version_file = save_blog_version(blog.folder_path, new_content, version_number)
606 |             
607 |             # Update blog with new content
608 |             blog.current_version = version_number
609 |             blog.latest_content = new_content
610 |             blog.updated_at = get_current_timestamp()
611 |             blog.status = BlogStatus.IN_PROGRESS
612 |             save_blogs_to_file()  # Save to persistent storage
613 |             
614 |             return APIResponse(
615 |                 success=True,
616 |                 message="Blog content updated successfully",
617 |                 data={
618 |                     "version": version_number,
619 |                     "content": new_content,
620 |                     "file_path": version_file
621 |                 }
622 |             )
623 |         else:
624 |             return APIResponse(
625 |                 success=True,
626 |                 message="No changes detected",
627 |                 data={
628 |                     "version": blog.current_version,
629 |                     "content": blog.latest_content
630 |                 }
631 |             )
632 |             
633 |     except HTTPException:
634 |         raise
635 |     except Exception as e:
636 |         raise HTTPException(status_code=500, detail=str(e))
637 | 
638 | @app.delete("/blogs/{blog_id}/versions/{version_num}", response_model=APIResponse)
639 | async def delete_blog_version(blog_id: str, version_num: int):
640 |     """Delete a specific blog version."""
641 |     try:
642 |         if blog_id not in blogs_db:
643 |             raise HTTPException(status_code=404, detail="Blog not found")
644 |         
645 |         blog = blogs_db[blog_id]
646 |         final_folder = Path(blog.folder_path) / "final"
647 |         version_file = final_folder / f"v{version_num}.md"
648 |         
649 |         if not version_file.exists():
650 |             raise HTTPException(status_code=404, detail="Version not found")
651 |         
652 |         # Don't allow deleting the current/latest version
653 |         if version_num == blog.current_version:
654 |             raise HTTPException(status_code=400, detail="Cannot delete the current version. Please create a new version first.")
655 |         
656 |         # Delete the version file
657 |         version_file.unlink()
658 |         
659 |         # If this was the latest content and we're deleting it, update to the highest remaining version
660 |         remaining_versions = list_blog_versions(blog.folder_path)
661 |         if remaining_versions:
662 |             # Find the highest version number
663 |             highest_version = max(v["version"] for v in remaining_versions)
664 |             if blog.current_version == version_num or blog.current_version > highest_version:
665 |                 # Update to the highest remaining version
666 |                 blog.current_version = highest_version
667 |                 # Load the content from the highest remaining version
668 |                 highest_version_file = final_folder / f"v{highest_version}.md"
669 |                 if highest_version_file.exists():
670 |                     with open(highest_version_file, 'r', encoding='utf-8') as f:
671 |                         blog.latest_content = f.read()
672 |                 blog.updated_at = get_current_timestamp()
673 |                 save_blogs_to_file()
674 |         
675 |         return APIResponse(
676 |             success=True,
677 |             message=f"Version {version_num} deleted successfully",
678 |             data={"deleted_version": version_num, "current_version": blog.current_version}
679 |         )
680 |         
681 |     except HTTPException:
682 |         raise
683 |     except Exception as e:
684 |         raise HTTPException(status_code=500, detail=str(e))
685 | 
686 | @app.post("/blogs/{blog_id}/generate", response_model=APIResponse)
687 | async def generate_blog_content(blog_id: str, request_data: dict):
688 |     """Generate new blog content using IBM watsonx AI."""
689 |     try:
690 |         if blog_id not in blogs_db:
691 |             raise HTTPException(status_code=404, detail="Blog not found")
692 |         
693 |         blog = blogs_db[blog_id]
694 |         prompt = request_data.get("prompt", "")
695 |         generation_type = request_data.get("generation_type", "text")  # Default to text only
696 |         
697 |         if not prompt:
698 |             raise HTTPException(status_code=400, detail="Prompt is required")
699 |             
700 |         # Force text-only generation (images disabled)
701 |         generation_type = "text"
702 |         
703 |         # Get IBM watsonx client
704 |         client = await get_watsonx_client()
705 |         if not client:
706 |             raise HTTPException(status_code=500, detail="IBM watsonx client not initialized")
707 |         
708 |         final_content = ""
709 |         images_generated = False
710 |         text_generated = False
711 |         log_id = ""
712 |         start_time = get_current_timestamp()
713 |         
714 |         try:
715 |             # Generate text content only (images disabled)
716 |             current_content_context = ""
717 |             if blog.latest_content:
718 |                 current_content_context = f"""
719 | 
720 | Current Blog Content:
721 | {blog.latest_content}
722 | 
723 | """
724 |             
725 |             enhanced_prompt = f"""You are an expert blog writer creating high-quality, engaging content for the blog titled: "{blog.title}"
726 |             
727 | Blog Description: {blog.description or "No description provided"}
728 | Tags: {', '.join(blog.tags) if blog.tags else "No tags"}
729 | Publication Site: {blog.publication_site or "General audience"}{current_content_context}
730 | User Request: {prompt}
731 | 
732 | IMPORTANT REQUIREMENTS:
733 | 1. Create professional, well-structured blog content that is engaging, informative, and optimized for the target audience
734 | 2. Use appropriate headings, bullet points, and formatting when relevant
735 | 3. Write in a clear, professional tone suitable for online publication
736 | 4. Focus purely on text content with excellent structure and flow
737 | 5. Create comprehensive, detailed content that stands on its own
738 | 6. Use markdown formatting for headers, lists, and emphasis
739 | 
740 | {f"Based on the current content above, " + prompt if blog.latest_content else prompt}"""
741 |             
742 |             # Log the request with the correct model from config
743 |             from services.watsonx_service.config import granite_config
744 |             log_id = log_watsonx_request(blog_id, enhanced_prompt, granite_config.model_id)
745 |             
746 |             # Generate content with IBM watsonx
747 |             generated_content = client.generate(enhanced_prompt)
748 |             
749 |             if not generated_content:
750 |                 raise Exception("IBM watsonx returned empty response")
751 |             
752 |             text_generated = True
753 |             
754 |             # Calculate processing time and log response
755 |             end_time = get_current_timestamp()
756 |             processing_time_ms = int((end_time - start_time).total_seconds() * 1000)
757 |             log_watsonx_response(log_id, generated_content, "", processing_time_ms)
758 |             
759 |             # Text-only generation (no images)
760 |             final_content = generated_content
761 |             
762 |             # Save the prompt
763 |             save_prompt(blog.folder_path, prompt)
764 |             
765 |             # Get next version number and save content
766 |             version_number = get_next_version_number(blog.folder_path)
767 |             version_file = save_blog_version(blog.folder_path, final_content, version_number)
768 |             
769 |             # Update blog with latest content
770 |             blog.current_version = version_number
771 |             blog.latest_content = final_content
772 |             blog.updated_at = get_current_timestamp()
773 |             blog.status = BlogStatus.IN_PROGRESS
774 |             save_blogs_to_file()  # Save to persistent storage
775 |             
776 |             # Success message for text-only generation
777 |             message = "Blog content generated successfully"
778 |             
779 |             return APIResponse(
780 |                 success=True,
781 |                 message=message,
782 |                 data={
783 |                     "version": version_number,
784 |                     "content": final_content,
785 |                     "file_path": version_file,
786 |                     "generation_type": "text",
787 |                     "text_generated": text_generated,
788 |                     "images_generated": False
789 |                 }
790 |             )
791 |             
792 |         except Exception as ai_error:
793 |             if log_id:
794 |                 end_time = get_current_timestamp()
795 |                 processing_time_ms = int((end_time - start_time).total_seconds() * 1000)
796 |                 log_watsonx_response(log_id, "", str(ai_error), processing_time_ms)
797 |             raise HTTPException(status_code=500, detail=f"AI generation error: {str(ai_error)}")
798 |         
799 |     except HTTPException:
800 |         raise
801 |     except Exception as e:
802 |         raise HTTPException(status_code=500, detail=str(e))
803 | 
804 | @app.post("/blogs/{blog_id}/comments", response_model=APIResponse)
805 | async def add_comment(blog_id: str, comment_data: CommentCreate):
806 |     """Add a comment to a blog."""
807 |     try:
808 |         if blog_id not in blogs_db:
809 |             raise HTTPException(status_code=404, detail="Blog not found")
810 |         
811 |         comment_id = generate_id()
812 |         comment = Comment(
813 |             id=comment_id,
814 |             blog_id=blog_id,
815 |             content=comment_data.content,
816 |             requested_changes=comment_data.requested_changes,
817 |             created_at=get_current_timestamp()
818 |         )
819 |         
820 |         if blog_id not in comments_db:
821 |             comments_db[blog_id] = []
822 |         comments_db[blog_id].append(comment)
823 |         save_comments_to_file()  # Save to persistent storage
824 |         
825 |         return APIResponse(
826 |             success=True,
827 |             message="Comment added successfully",
828 |             data=comment.model_dump(mode='json')
829 |         )
830 |     except HTTPException:
831 |         raise
832 |     except Exception as e:
833 |         raise HTTPException(status_code=500, detail=str(e))
834 | 
835 | @app.get("/blogs/{blog_id}/comments", response_model=APIResponse)
836 | async def get_blog_comments(blog_id: str):
837 |     """Get all comments for a blog."""
838 |     try:
839 |         if blog_id not in blogs_db:
840 |             raise HTTPException(status_code=404, detail="Blog not found")
841 |         
842 |         comments = comments_db.get(blog_id, [])
843 |         comments_list = [comment.model_dump(mode='json') for comment in comments]
844 |         
845 |         return APIResponse(
846 |             success=True,
847 |             message="Comments retrieved successfully",
848 |             data=comments_list
849 |         )
850 |     except HTTPException:
851 |         raise
852 |     except Exception as e:
853 |         raise HTTPException(status_code=500, detail=str(e))
854 | 
855 | if __name__ == "__main__":
856 |     import uvicorn
857 |     uvicorn.run(app, host="0.0.0.0", port=settings.blog_service_port)
</content>
</file>
</files>
<environment_details>
# VSCode Visible Files
requirements.txt

# VSCode Open Tabs
start_all_services.py,requirements.txt,services/blog_service/main.py,.env

# Actively Running Terminals
## Terminal 1 (Active)
### Working Directory: `c:\workspace\ForgeByBob`
### Original command: `Stop-Process -Name python -Force -ErrorAction SilentlyContinue; Start-Sleep -Seconds 2; python start_all_services.py`
## Terminal 2 (Active)
### Working Directory: `c:\workspace\ForgeByBob`
### Original command: `python start_all_services.py`
## Terminal 3 (Active)
### Working Directory: `c:\workspace\ForgeByBob`
### Original command: `Stop-Process -Name python -Force -ErrorAction SilentlyContinue; Start-Sleep -Seconds 2; python start_all_services.py`
## Terminal 4 (Active)
### Working Directory: `c:\workspace\ForgeByBob`
### Original command: `python start_all_services.py`
## Terminal 5 (Active)
### Working Directory: `c:\workspace\ForgeByBob`
### Original command: `Stop-Process -Name python -Force -ErrorAction SilentlyContinue; Start-Sleep -Seconds 3; python start_all_services.py`

# Current Time
Current time in ISO 8601 UTC format: 2026-05-02T04:39:34.356Z
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

I found the issue! Looking at the code, I can see that when a blog is created, the `latest_content` field is not being set initially. Then when you try to display it on the blog detail page, it's empty.

Let me check the blog detail template to confirm how it's trying to display the content:

<read_file>
<args>
<file>
<path>services/ui_service/templates/blog_detail.html</path>
</file>
</args>
</read_file>

---

**User:**

[read_file for 'services/ui_service/templates/blog_detail.html'. Reading multiple files at once is more efficient for the LLM. If other files are relevant to your current task, please read them simultaneously.] Result:
<files>
<file><path>services/ui_service/templates/blog_detail.html</path>
<content lines="1-488">
  1 | {% extends "base.html" %}
  2 | 
  3 | {% block title %}{{ blog.title }} - Blog Writer{% endblock %}
  4 | 
  5 | {% block content %}
  6 | <!-- Success/Error Messages -->
  7 | {% set success_msg = request.query_params.get('success') %}
  8 | {% set error_msg = request.query_params.get('error') %}
  9 | 
 10 | {% if success_msg %}
 11 | <div style="background: #d4edda; color: #155724; padding: 1rem; border-radius: 4px; margin-bottom: 1rem; border: 1px solid #c3e6cb;">
 12 |     ✓ {{ success_msg }}
 13 | </div>
 14 | {% endif %}
 15 | 
 16 | {% if error_msg %}
 17 | <div style="background: #f8d7da; color: #721c24; padding: 1rem; border-radius: 4px; margin-bottom: 1rem; border: 1px solid #f5c6cb;">
 18 |     ✗ {{ error_msg }}
 19 | </div>
 20 | {% endif %}
 21 | 
 22 | <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 2rem;">
 23 |     <div>
 24 |         <h2>{{ blog.title }}</h2>
 25 |         <div class="blog-meta">
 26 |             <span class="status status-{{ blog.status }}">{{ blog.status|replace('_', ' ')|title }}</span>
 27 |             <span style="margin-left: 1rem;">Created: {{ blog.created_at[:10] }}</span>
 28 |             {% if blog.current_version > 0 %}
 29 |             <span style="margin-left: 1rem;">Current Version: {{ blog.current_version }}</span>
 30 |             {% endif %}
 31 |         </div>
 32 |     </div>
 33 |     <a href="/" class="btn" style="background: #95a5a6;">Back to Home</a>
 34 | </div>
 35 | 
 36 | {% if blog.description %}
 37 | <div class="card">
 38 |     <h4>Description</h4>
 39 |     <p>{{ blog.description }}</p>
 40 | </div>
 41 | {% endif %}
 42 | 
 43 | <!-- Latest Content -->
 44 | {% if blog.latest_content %}
 45 | <div class="card">
 46 |     <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1rem;">
 47 |         <h4>Latest Content (Version {{ blog.current_version }})</h4>
 48 |         <div style="display: flex; gap: 0.5rem;">
 49 |             <button onclick="copyContentForMedium()" class="btn" style="background: #2ecc71; color: white;" title="Copy formatted content for Medium/blogs">
 50 |                 Copy for Medium
 51 |             </button>
 52 |             <button onclick="copyMarkdownContent()" class="btn" style="background: #9b59b6; color: white;" title="Copy raw markdown">
 53 |                 Copy Markdown
 54 |             </button>
 55 |             <button onclick="toggleEditMode()" class="btn" style="background: #f39c12; color: white;" id="edit-toggle-btn">
 56 |                 Edit Content
 57 |             </button>
 58 |         </div>
 59 |     </div>
 60 |     
 61 |     <!-- Display Mode -->
 62 |     <div id="content-display" style="background: #f8f9fa; padding: 1.5rem; border-radius: 4px; max-height: 400px; overflow-y: auto; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; line-height: 1.6; border-left: 4px solid #27ae60;">
 63 |         <div id="rendered-content"></div>
 64 |     </div>
 65 |     
 66 |     <!-- Hidden content storage for JavaScript with proper escaping -->
 67 |     <textarea id="blog-content-data" style="display: none;">{{ blog.latest_content }}</textarea>
 68 |     
 69 |     <!-- Edit Mode -->
 70 |     <div id="content-edit" style="display: none;">
 71 |         <form method="post" action="/blog/{{ blog.id }}/content" id="content-form">
 72 |             <div class="form-group">
 73 |                 <textarea id="content-editor" name="content" style="width: 100%; min-height: 400px; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; line-height: 1.6; padding: 1rem; border: 1px solid #ddd; border-radius: 4px;">{{ blog.latest_content }}</textarea>
 74 |             </div>
 75 |             <div style="margin-top: 1rem;">
 76 |                 <button type="submit" class="btn btn-success">Save Content</button>
 77 |                 <button type="button" onclick="cancelEdit()" class="btn" style="background: #95a5a6; margin-left: 0.5rem;">Cancel</button>
 78 |             </div>
 79 |         </form>
 80 |     </div>
 81 | </div>
 82 | {% else %}
 83 | <div class="card">
 84 |     <h4>Latest Content</h4>
 85 |     <p style="color: #666;">No content available yet. Generate your first content below.</p>
 86 | </div>
 87 | {% endif %}
 88 | 
 89 | <!-- Generate Content Section -->
 90 | <div class="card">
 91 |     <h4>Generate New Content with IBM watsonx.ai</h4>
 92 |     <form method="post" action="/blog/{{ blog.id }}/generate">
 93 |         <div class="form-group">
 94 |             <label for="prompt">Prompt for AI Generation</label>
 95 |             <textarea id="prompt" name="prompt" required placeholder="Describe what you want to generate or modify in your blog content..."></textarea>
 96 |             <p style="font-size: 0.9rem; color: #666; margin-top: 0.5rem;">
 97 |                 💡 <strong>Tip:</strong> Be specific about what you want. IBM watsonx.ai will generate high-quality text content based on your prompt.
 98 |             </p>
 99 |         </div>
100 |         <div style="display: flex; gap: 10px; flex-wrap: wrap;">
101 |             <button type="submit" name="generation_type" value="text" class="btn btn-primary">Generate Content</button>
102 |         </div>
103 |         <p style="font-size: 0.85rem; color: #999; margin-top: 0.5rem;">
104 |             ⚠️ Note: Free tier has rate limits. Wait 5 minutes between requests if you encounter errors.
105 |         </p>
106 |     </form>
107 | </div>
108 | 
109 | <!-- Blog Versions -->
110 | {% if versions %}
111 | <div class="card">
112 |     <h4>Content Versions</h4>
113 |     <div style="max-height: 600px; overflow-y: auto;">
114 |         {% for version in versions %}
115 |         <div style="border: 1px solid #ddd; border-radius: 4px; padding: 1rem; margin-bottom: 1rem;">
116 |             <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.5rem;">
117 |                 <div>
118 |                     <strong>Version {{ version.version }}</strong>
119 |                     {% if version.version == blog.current_version %}
120 |                     <span style="background: #27ae60; color: white; padding: 0.2rem 0.5rem; border-radius: 3px; font-size: 0.7rem; margin-left: 0.5rem;">CURRENT</span>
121 |                     {% endif %}
122 |                 </div>
123 |                 <div style="display: flex; gap: 0.5rem; align-items: center;">
124 |                     <span style="color: #666; font-size: 0.9rem;">{{ version.created_at[:19] if version.created_at else 'Unknown' }}</span>
125 |                     <button onclick="toggleContent({{ version.version }})" class="btn" style="background: #3498db; color: white; padding: 0.25rem 0.5rem; font-size: 0.8rem;">
126 |                         <span id="toggle-text-{{ version.version }}">Show Content</span>
127 |                     </button>
128 |                     <button onclick="copyVersionContent({{ version.version }})" class="btn" style="background: #9b59b6; color: white; padding: 0.25rem 0.5rem; font-size: 0.8rem;" title="Copy this version">
129 |                         Copy
130 |                     </button>
131 |                     {% if version.version != blog.current_version %}
132 |                     <button onclick="confirmDelete({{ version.version }})" class="btn" style="background: #e74c3c; color: white; padding: 0.25rem 0.5rem; font-size: 0.8rem;" title="Delete this version">
133 |                         Delete
134 |                     </button>
135 |                     {% endif %}
136 |                 </div>
137 |             </div>
138 |             <div id="content-{{ version.version }}" style="display: none; background: #f8f9fa; padding: 1rem; border-radius: 4px; max-height: 300px; overflow-y: auto; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; line-height: 1.6;">
139 |                 <div style="text-align: center; color: #666;">Loading content...</div>
140 |             </div>
141 |             <div style="color: #666; font-size: 0.9rem; margin-top: 0.5rem; display: flex; justify-content: space-between;">
142 |                 <span>Size: {{ version.size }} bytes</span>
143 |                 {% if version.version != blog.current_version %}
144 |                 <span style="color: #e74c3c; font-size: 0.8rem;">⚠️ Can be deleted</span>
145 |                 {% endif %}
146 |             </div>
147 |         </div>
148 |         {% endfor %}
149 |     </div>
150 | </div>
151 | {% else %}
152 | <div class="card">
153 |     <h4>Content Versions</h4>
154 |     <p style="color: #666;">No content versions yet. Generate your first version above.</p>
155 | </div>
156 | {% endif %}
157 | 
158 | <script>
159 | // Function to render markdown content with images
160 | function renderMarkdownContent(content) {
161 |     if (!content) return '';
162 |     
163 |     let renderedContent = content;
164 |     
165 |     // Convert markdown images to HTML images with fallback
166 |     const imageRegex = /!\[([^\]]*)\]\(([^)]+)\)/g;
167 |     renderedContent = renderedContent.replace(imageRegex, (match, altText, url) => {
168 |         const randomId = Math.floor(Math.random() * 1000);
169 |         const fallbackUrl = `https://picsum.photos/600/400?random=${randomId}`;
170 |         const svgFallback = `data:image/svg+xml;base64,${btoa(`<svg xmlns="http://www.w3.org/2000/svg" width="600" height="400"><rect width="100%" height="100%" fill="#f0f0f0"/><text x="50%" y="50%" font-family="Arial" font-size="20" fill="#666" text-anchor="middle" dy=".3em">${altText || 'Image'}</text></svg>`)}`;
171 |         
172 |         return `<img src="${url.trim()}" alt="${altText}" 
173 |                 style="max-width: 100%; height: auto; margin: 1rem 0; border-radius: 4px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); display: block;" 
174 |                 onerror="if(this.src!=='${fallbackUrl}') { this.src='${fallbackUrl}'; } else { this.src='${svgFallback}'; }">`;
175 |     });
176 |     
177 |     // Convert markdown headers
178 |     renderedContent = renderedContent.replace(/^### (.*$)/gim, '<h3 style="color: #2c3e50; margin-top: 1.5rem; margin-bottom: 0.5rem;">$1</h3>');
179 |     renderedContent = renderedContent.replace(/^## (.*$)/gim, '<h2 style="color: #2c3e50; margin-top: 1.5rem; margin-bottom: 0.5rem;">$1</h2>');
180 |     renderedContent = renderedContent.replace(/^# (.*$)/gim, '<h1 style="color: #2c3e50; margin-top: 1.5rem; margin-bottom: 0.5rem;">$1</h1>');
181 |     
182 |     // Convert markdown bold and italic
183 |     renderedContent = renderedContent.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');
184 |     renderedContent = renderedContent.replace(/\*(.*?)\*/g, '<em>$1</em>');
185 |     
186 |     // Convert markdown bullet points (handle multiline lists better)
187 |     const lines = renderedContent.split('\n');
188 |     let inList = false;
189 |     let processedLines = [];
190 |     
191 |     for (let i = 0; i < lines.length; i++) {
192 |         const line = lines[i];
193 |         if (line.match(/^- /)) {
194 |             if (!inList) {
195 |                 processedLines.push('<ul style="margin: 0.5rem 0; padding-left: 1.5rem;">');
196 |                 inList = true;
197 |             }
198 |             processedLines.push('<li style="margin-bottom: 0.25rem;">' + line.substring(2) + '</li>');
199 |         } else {
200 |             if (inList) {
201 |                 processedLines.push('</ul>');
202 |                 inList = false;
203 |             }
204 |             processedLines.push(line);
205 |         }
206 |     }
207 |     
208 |     if (inList) {
209 |         processedLines.push('</ul>');
210 |     }
211 |     
212 |     renderedContent = processedLines.join('\n');
213 |     
214 |     // Convert line breaks to paragraphs (improved handling)
215 |     const paragraphs = renderedContent.split('\n\n');
216 |     renderedContent = paragraphs.map(p => {
217 |         const trimmed = p.trim();
218 |         if (trimmed && !trimmed.includes('<h') && !trimmed.includes('<img') && !trimmed.includes('<ul') && !trimmed.includes('<li')) {
219 |             // Handle single line breaks within paragraphs
220 |             const withBreaks = trimmed.replace(/\n/g, '<br>');
221 |             return `<p style="margin-bottom: 1rem; line-height: 1.6;">${withBreaks}</p>`;
222 |         }
223 |         return trimmed;
224 |     }).join('\n\n');
225 |     
226 |     return renderedContent;
227 | }
228 | 
229 | // Initialize content rendering when page loads
230 | document.addEventListener('DOMContentLoaded', function() {
231 |     const contentDiv = document.getElementById('rendered-content');
232 |     const contentElement = document.getElementById('blog-content-data');
233 |     
234 |     if (contentElement) {
235 |         const originalContent = contentElement.value;
236 |         
237 |         if (originalContent && originalContent.trim() !== '') {
238 |             const renderedHTML = renderMarkdownContent(originalContent);
239 |             contentDiv.innerHTML = renderedHTML;
240 |         } else {
241 |             contentDiv.innerHTML = '<p style="color: #666;">No content available</p>';
242 |         }
243 |     } else {
244 |         contentDiv.innerHTML = '<p style="color: #666;">Content element not found</p>';
245 |     }
246 | });
247 | 
248 | let isEditMode = false;
249 | 
250 | // Copy functions for content sharing
251 | function copyContentForMedium() {
252 |     const contentElement = document.getElementById('blog-content-data');
253 |     
254 |     if (!contentElement) {
255 |         alert('No content to copy');
256 |         return;
257 |     }
258 |     
259 |     const originalContent = contentElement.value;
260 |     
261 |     // Convert markdown to Medium-friendly format
262 |     let mediumContent = originalContent;
263 |     
264 |     // Keep images as markdown - Medium supports markdown images
265 |     // No changes needed for images as Medium editor accepts ![alt](url) format
266 |     
267 |     // Headers - Medium uses # for headers, keep as-is
268 |     // Bold and italic - Medium uses ** and *, keep as-is
269 |     
270 |     // Add some formatting notes for user
271 |     const copyText = `${mediumContent}
272 | 
273 | ---
274 | 📝 Note: This content includes images and is formatted for Medium. 
275 | - Images will render automatically when pasted into Medium editor
276 | - All formatting (headers, bold, italic) is preserved
277 | - Copy this entire text including the images`;
278 |     
279 |     // Copy to clipboard
280 |     navigator.clipboard.writeText(copyText).then(() => {
281 |         showCopyMessage('Content copied for Medium! Paste directly into Medium editor - images will render automatically.');
282 |     }).catch(err => {
283 |         console.error('Failed to copy: ', err);
284 |         alert('Failed to copy content');
285 |     });
286 | }
287 | 
288 | function copyMarkdownContent() {
289 |     const contentElement = document.getElementById('blog-content-data');
290 |     
291 |     if (!contentElement) {
292 |         alert('No content to copy');
293 |         return;
294 |     }
295 |     
296 |     const originalContent = contentElement.value;
297 |     
298 |     // Copy raw markdown
299 |     navigator.clipboard.writeText(originalContent).then(() => {
300 |         showCopyMessage('Markdown content copied to clipboard!');
301 |     }).catch(err => {
302 |         console.error('Failed to copy: ', err);
303 |         alert('Failed to copy content');
304 |     });
305 | }
306 | 
307 | function showCopyMessage(message) {
308 |     // Create a temporary message
309 |     const messageDiv = document.createElement('div');
310 |     messageDiv.style.cssText = `
311 |         position: fixed;
312 |         top: 20px;
313 |         right: 20px;
314 |         background: #27ae60;
315 |         color: white;
316 |         padding: 1rem;
317 |         border-radius: 4px;
318 |         z-index: 1000;
319 |         box-shadow: 0 2px 10px rgba(0,0,0,0.2);
320 |     `;
321 |     messageDiv.textContent = message;
322 |     document.body.appendChild(messageDiv);
323 |     
324 |     // Remove after 3 seconds
325 |     setTimeout(() => {
326 |         document.body.removeChild(messageDiv);
327 |     }, 3000);
328 | }
329 | 
330 | async function copyVersionContent(version) {
331 |     try {
332 |         const response = await fetch(`/api/blogs/{{ blog.id }}/versions/${version}/content`);
333 |         const data = await response.json();
334 |         
335 |         if (data.success && data.data && data.data.content) {
336 |             navigator.clipboard.writeText(data.data.content).then(() => {
337 |                 showCopyMessage(`Version ${version} content copied to clipboard!`);
338 |             }).catch(err => {
339 |                 console.error('Failed to copy: ', err);
340 |                 alert('Failed to copy content');
341 |             });
342 |         } else {
343 |             alert('Failed to load content for copying');
344 |         }
345 |     } catch (error) {
346 |         console.error('Error loading content: ', error);
347 |         alert('Error loading content for copying');
348 |     }
349 | }
350 | 
351 | function toggleEditMode() {
352 |     const displayDiv = document.getElementById('content-display');
353 |     const editDiv = document.getElementById('content-edit');
354 |     const toggleBtn = document.getElementById('edit-toggle-btn');
355 |     
356 |     if (!isEditMode) {
357 |         // Enter edit mode
358 |         displayDiv.style.display = 'none';
359 |         editDiv.style.display = 'block';
360 |         toggleBtn.textContent = 'Cancel Edit';
361 |         toggleBtn.style.background = '#e74c3c';
362 |         isEditMode = true;
363 |     } else {
364 |         // Exit edit mode
365 |         displayDiv.style.display = 'block';
366 |         editDiv.style.display = 'none';
367 |         toggleBtn.textContent = 'Edit Content';
368 |         toggleBtn.style.background = '#f39c12';
369 |         isEditMode = false;
370 |     }
371 | }
372 | 
373 | function cancelEdit() {
374 |     // Reset the textarea to original content and exit edit mode
375 |     const originalContent = document.getElementById('content-display').textContent;
376 |     document.getElementById('content-editor').value = originalContent;
377 |     toggleEditMode();
378 | }
379 | 
380 | function confirmDelete(version) {
381 |     if (confirm(`Are you sure you want to delete Version ${version}? This action cannot be undone.`)) {
382 |         // Create and submit a hidden form for deletion
383 |         const form = document.createElement('form');
384 |         form.method = 'POST';
385 |         form.action = `/blog/{{ blog.id }}/versions/${version}/delete`;
386 |         form.style.display = 'none';
387 |         document.body.appendChild(form);
388 |         form.submit();
389 |     }
390 | }
391 | 
392 | async function toggleContent(version) {
393 |     const contentDiv = document.getElementById(`content-${version}`);
394 |     const toggleText = document.getElementById(`toggle-text-${version}`);
395 |     
396 |     if (contentDiv.style.display === 'none') {
397 |         // Show content
398 |         contentDiv.style.display = 'block';
399 |         toggleText.textContent = 'Hide Content';
400 |         
401 |         // Load content if not already loaded
402 |         if (contentDiv.innerHTML.includes('Loading content...')) {
403 |             try {
404 |                 const response = await fetch(`/api/blogs/{{ blog.id }}/versions/${version}/content`);
405 |                 const data = await response.json();
406 |                 
407 |                 if (data.success && data.data && data.data.content) {
408 |                     contentDiv.innerHTML = renderMarkdownContent(data.data.content);
409 |                 } else {
410 |                     contentDiv.innerHTML = '<div style="color: #d32f2f;">Failed to load content</div>';
411 |                 }
412 |             } catch (error) {
413 |                 contentDiv.innerHTML = '<div style="color: #d32f2f;">Error loading content: ' + error.message + '</div>';
414 |             }
415 |         }
416 |     } else {
417 |         // Hide content
418 |         contentDiv.style.display = 'none';
419 |         toggleText.textContent = 'Show Content';
420 |     }
421 | }
422 | </script>
423 | 
424 | <!-- Comments and Feedback -->
425 | <div class="card">
426 |     <h4>Comments and Feedback</h4>
427 |     
428 |     <!-- Add Comment Form -->
429 |     <form method="post" action="/blog/{{ blog.id }}/comment" style="margin-bottom: 2rem;">
430 |         <div class="form-group">
431 |             <label for="content">Comment</label>
432 |             <textarea id="content" name="content" required placeholder="Add your feedback or comments..."></textarea>
433 |         </div>
434 |         <div class="form-group">
435 |             <label for="requested_changes">Requested Changes (optional)</label>
436 |             <textarea id="requested_changes" name="requested_changes" placeholder="Specific changes you'd like to see in the next version..."></textarea>
437 |         </div>
438 |         <button type="submit" class="btn btn-primary">Add Comment</button>
439 |     </form>
440 |     
441 |     <!-- Comments List -->
442 |     {% if comments %}
443 |         {% for comment in comments %}
444 |         <div style="border-left: 4px solid #3498db; padding-left: 1rem; margin-bottom: 1.5rem;">
445 |             <div style="color: #666; font-size: 0.9rem; margin-bottom: 0.5rem;">
446 |                 {{ comment.created_at[:16] if comment.created_at else 'Unknown time' }}
447 |             </div>
448 |             <div style="margin-bottom: 0.5rem;">{{ comment.content }}</div>
449 |             {% if comment.requested_changes %}
450 |             <div style="background: #fff3cd; padding: 0.5rem; border-radius: 4px; font-size: 0.9rem;">
451 |                 <strong>Requested Changes:</strong> {{ comment.requested_changes }}
452 |             </div>
453 |             {% endif %}
454 |         </div>
455 |         {% endfor %}
456 |     {% else %}
457 |         <p style="color: #666;">No comments yet. Add the first comment above.</p>
458 |     {% endif %}
459 | </div>
460 | 
461 | {% if blog.tags %}
462 | <div class="card">
463 |     <h4>Tags</h4>
464 |     <div>
465 |         {% for tag in blog.tags %}
466 |         <span style="background: #ecf0f1; padding: 0.25rem 0.5rem; border-radius: 4px; font-size: 0.9rem; margin-right: 0.5rem;">{{ tag }}</span>
467 |         {% endfor %}
468 |     </div>
469 | </div>
470 | {% endif %}
471 | 
472 | <script>
473 | // Check for URL parameters to show messages
474 | const urlParams = new URLSearchParams(window.location.search);
475 | if (urlParams.get('error')) {
476 |     const errorDiv = document.createElement('div');
477 |     errorDiv.className = 'alert alert-error';
478 |     errorDiv.textContent = urlParams.get('error');
479 |     document.querySelector('.container').insertBefore(errorDiv, document.querySelector('.container').firstChild);
480 | }
481 | if (urlParams.get('success')) {
482 |     const successDiv = document.createElement('div');
483 |     successDiv.className = 'alert alert-success';
484 |     successDiv.textContent = 'Operation completed successfully!';
485 |     document.querySelector('.container').insertBefore(successDiv, document.querySelector('.container').firstChild);
486 | }
487 | </script>
488 | {% endblock %}
</content>
</file>
</files>
<environment_details>
# VSCode Visible Files
requirements.txt

# VSCode Open Tabs
start_all_services.py,requirements.txt,services/blog_service/main.py,.env

# Actively Running Terminals
## Terminal 1 (Active)
### Working Directory: `c:\workspace\ForgeByBob`
### Original command: `Stop-Process -Name python -Force -ErrorAction SilentlyContinue; Start-Sleep -Seconds 2; python start_all_services.py`
## Terminal 2 (Active)
### Working Directory: `c:\workspace\ForgeByBob`
### Original command: `python start_all_services.py`
## Terminal 3 (Active)
### Working Directory: `c:\workspace\ForgeByBob`
### Original command: `Stop-Process -Name python -Force -ErrorAction SilentlyContinue; Start-Sleep -Seconds 2; python start_all_services.py`
## Terminal 4 (Active)
### Working Directory: `c:\workspace\ForgeByBob`
### Original command: `python start_all_services.py`
## Terminal 5 (Active)
### Working Directory: `c:\workspace\ForgeByBob`
### Original command: `Stop-Process -Name python -Force -ErrorAction SilentlyContinue; Start-Sleep -Seconds 3; python start_all_services.py`

# Current Time
Current time in ISO 8601 UTC format: 2026-05-02T04:39:44.552Z
User time zone: America/New_York, UTC-4:00

# Current Cost
$0.07

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

Now I can see the issue! The problem is in the `blog_detail.html` template at line 44. It checks `{% if blog.latest_content %}` to display the Latest Content section. However, when a blog is first created in `services/blog_service/main.py`, the `latest_content` field is not initialized (it defaults to `None`).

The `latest_content` only gets populated when content is generated (line 771 in `main.py`). So for newly created blogs that haven't had content generated yet, the Latest Content section won't show up.

Let me check the Blog model to understand the field definition:

<read_file>
<args>
<file>
<path>shared/models.py</path>
</file>
</args>
</read_file>

---

**User:**

[read_file for 'shared/models.py'. Reading multiple files at once is more efficient for the LLM. If other files are relevant to your current task, please read them simultaneously.] Result:
<files>
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
requirements.txt

# VSCode Open Tabs
start_all_services.py,requirements.txt,services/blog_service/main.py,.env

# Actively Running Terminals
## Terminal 1 (Active)
### Working Directory: `c:\workspace\ForgeByBob`
### Original command: `Stop-Process -Name python -Force -ErrorAction SilentlyContinue; Start-Sleep -Seconds 2; python start_all_services.py`
## Terminal 2 (Active)
### Working Directory: `c:\workspace\ForgeByBob`
### Original command: `python start_all_services.py`
## Terminal 3 (Active)
### Working Directory: `c:\workspace\ForgeByBob`
### Original command: `Stop-Process -Name python -Force -ErrorAction SilentlyContinue; Start-Sleep -Seconds 2; python start_all_services.py`
## Terminal 4 (Active)
### Working Directory: `c:\workspace\ForgeByBob`
### Original command: `python start_all_services.py`
## Terminal 5 (Active)
### Working Directory: `c:\workspace\ForgeByBob`
### Original command: `Stop-Process -Name python -Force -ErrorAction SilentlyContinue; Start-Sleep -Seconds 3; python start_all_services.py`

# Current Time
Current time in ISO 8601 UTC format: 2026-05-02T04:39:55.884Z
User time zone: America/New_York, UTC-4:00

# Current Cost
$0.14

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

Perfect! I found the issue. The `latest_content` field in the Blog model (line 48 in `shared/models.py`) is `Optional[str] = None`, which means it's `None` by default when a blog is created.

The problem is that the template checks `{% if blog.latest_content %}` which evaluates to `False` when `latest_content` is `None` or an empty string. This causes the "Latest Content" section to not display at all for newly created blogs.

The fix is to initialize `latest_content` with an empty string instead of `None` when creating a blog. Let me update the blog creation code:

<apply_diff>
<path>services/blog_service/main.py</path>
<diff>
<<<<<<< SEARCH
:start_line:420
-------
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
=======
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
>>>>>>> REPLACE
</diff>
</apply_diff>

---

**User:**

[apply_diff for 'services/blog_service/main.py'] Result:
<file_write_result>
<path>services/blog_service/main.py</path>
<operation>modified</operation>
<problems>

New problems detected after saving the file:
services/blog_service/main.py
- [basedpyright Error] 179 |         return None : Type "None" is not assignable to return type "str"
  "None" is not assignable to "str"
- [basedpyright Error] 182 |         return None : Type "None" is not assignable to return type "str"
  "None" is not assignable to "str"
- [basedpyright Error] 325 | def log_watsonx_response(log_id: str, response_content: str = None, error_message: str = None, processing_time_ms: int = None): : Expression of type "None" cannot be assigned to parameter of type "str"
  "None" is not assignable to "str"
- [basedpyright Error] 325 | def log_watsonx_response(log_id: str, response_content: str = None, error_message: str = None, processing_time_ms: int = None): : Expression of type "None" cannot be assigned to parameter of type "str"
  "None" is not assignable to "str"
- [basedpyright Error] 325 | def log_watsonx_response(log_id: str, response_content: str = None, error_message: str = None, processing_time_ms: int = None): : Expression of type "None" cannot be assigned to parameter of type "int"
  "None" is not assignable to "int"</problems>
<notice>
<i>You do not need to re-read the file, as you have seen all changes</i>
<i>Proceed with the task using these changes as the new baseline.</i>
</notice>
</file_write_result>

<notice>Making multiple related changes in a single apply_diff is more efficient. If other changes are needed in this file, please include them as additional SEARCH/REPLACE blocks.</notice>
<environment_details>
# VSCode Visible Files
services\blog_service\main.py

# VSCode Open Tabs
start_all_services.py,requirements.txt,services/blog_service/main.py,.env

# Recently Modified Files
These files have been modified since you last accessed them (file was just edited so you may need to re-read it before editing):
services/blog_service/main.py

# Actively Running Terminals
## Terminal 1 (Active)
### Working Directory: `c:\workspace\ForgeByBob`
### Original command: `Stop-Process -Name python -Force -ErrorAction SilentlyContinue; Start-Sleep -Seconds 2; python start_all_services.py`
## Terminal 2 (Active)
### Working Directory: `c:\workspace\ForgeByBob`
### Original command: `python start_all_services.py`
## Terminal 3 (Active)
### Working Directory: `c:\workspace\ForgeByBob`
### Original command: `Stop-Process -Name python -Force -ErrorAction SilentlyContinue; Start-Sleep -Seconds 2; python start_all_services.py`
## Terminal 4 (Active)
### Working Directory: `c:\workspace\ForgeByBob`
### Original command: `python start_all_services.py`
## Terminal 5 (Active)
### Working Directory: `c:\workspace\ForgeByBob`
### Original command: `Stop-Process -Name python -Force -ErrorAction SilentlyContinue; Start-Sleep -Seconds 3; python start_all_services.py`

# Current Time
Current time in ISO 8601 UTC format: 2026-05-02T04:40:15.667Z
User time zone: America/New_York, UTC-4:00

# Current Cost
$0.23

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

Good! The change has been applied. Now I need to restart the services so the change takes effect. The type errors shown are pre-existing issues in the code and not related to our fix. Let me restart the services:

<execute_command>
<command>Stop-Process -Name python -Force -ErrorAction SilentlyContinue; Start-Sleep -Seconds 3; python start_all_services.py</command>
</execute_command>

