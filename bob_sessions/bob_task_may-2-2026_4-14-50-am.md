**User:**

<task>
In write agen manual run success call not saved in Home, your blog. also the api call not showing in aoi log
</task>
<environment_details>
# VSCode Visible Files


# VSCode Open Tabs
.vscode/settings.json,services/ui_service/templates/home.html,.bobalytics.json,.gitignore,services/orchestration_service/agent_base.py,services/orchestration_service/agents/publisher_agent.py,services/orchestration_service/agent_registry.py,stop_all_services.py,services/ui_service/main.py,services/orchestration_service/main.py,services/ui_service/templates/agent_dashboard.html,services/orchestration_service/agents/writer_agent.py,services/orchestration_service/pipeline_manager.py,test_agent_metadata.py,test_orchestration.py,enhancement1_B_delta_agent_dashboard.md,services/ui_service/templates/base.html,services/ui_service/templates/create.html,services/api_gateway/main.py,services/orchestration_service/agents/__init__.py

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
### New Output
INFO:     127.0.0.1:58944 - "GET /api/blogs HTTP/1.1" 200 OK
INFO:     127.0.0.1:58815 - "GET / HTTP/1.1" 200 OK
INFO:     127.0.0.1:58815 - "GET /.well-known/appspecific/com.chrome.devtools.json HTTP/1.1" 404 Not Found


# Current Time
Current time in ISO 8601 UTC format: 2026-05-02T08:12:01.287Z
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

I'll help you investigate and fix the issues with the writer agent manual run not saving to Home/blog and API calls not showing in logs. Let me start by examining the relevant files.

<read_file>
<args>
<file>
<path>services/orchestration_service/agents/writer_agent.py</path>
</file>
<file>
<path>services/ui_service/templates/agent_dashboard.html</path>
</file>
<file>
<path>services/api_gateway/main.py</path>
</file>
<file>
<path>services/blog_service/main.py</path>
</file>
<file>
<path>services/orchestration_service/pipeline_manager.py</path>
</file>
</args>
</read_file>

---

**User:**

[read_file for 5 files] Result:
<files>
<file><path>services/orchestration_service/agents/writer_agent.py</path>
<content lines="1-185">
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
 13 | # Blog service URL
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
 74 |             # Construct full prompt
 75 |             full_prompt = f"Topic: {prompt}\n\n"
 76 |             
 77 |             if research_brief:
 78 |                 full_prompt += f"Research Context:\n{research_brief}\n\n"
 79 |             
 80 |             full_prompt += f"Tone: {tone}\n\n"
 81 |             full_prompt += "Write a complete blog post with title, introduction, body, and conclusion."
 82 |             
 83 |             logger.info(f"WriterAgent: Generating content for prompt: {prompt[:50]}...")
 84 |             
 85 |             # Generate content
 86 |             content = self.granite.generate(
 87 |                 prompt=full_prompt,
 88 |                 system_prompt=self.system_prompt,
 89 |                 max_tokens=2048,
 90 |                 temperature=0.7
 91 |             )
 92 |             
 93 |             logger.info(f"WriterAgent: Generated {len(content)} characters")
 94 |             
 95 |             # Extract title from content (first line or first heading)
 96 |             title = "Untitled Blog"
 97 |             content_lines = content.strip().split('\n')
 98 |             for line in content_lines:
 99 |                 line = line.strip()
100 |                 if line:
101 |                     # Remove markdown heading markers
102 |                     title = line.lstrip('#').strip()
103 |                     break
104 |             
105 |             # Create draft blog via blog service
106 |             blog_id = None
107 |             blog_created = False
108 |             
109 |             try:
110 |                 async with httpx.AsyncClient(timeout=30.0) as client:
111 |                     # Create blog draft
112 |                     blog_data = {
113 |                         "title": title,
114 |                         "description": f"Generated from prompt: {prompt[:100]}",
115 |                         "tags": ["ai-generated", "draft"],
116 |                         "publication_site": "Blog Platform",
117 |                         "initial_prompt": prompt
118 |                     }
119 |                     
120 |                     logger.info(f"WriterAgent: Creating draft blog via API...")
121 |                     create_response = await client.post(
122 |                         f"{BLOG_SERVICE_URL}/blogs",
123 |                         json=blog_data
124 |                     )
125 |                     
126 |                     if create_response.status_code == 200:
127 |                         create_result = create_response.json()
128 |                         if create_result.get("success"):
129 |                             blog_id = create_result["data"]["id"]
130 |                             blog_created = True
131 |                             logger.info(f"WriterAgent: Created draft blog {blog_id}")
132 |                             
133 |                             # Update blog content
134 |                             content_data = {"content": content}
135 |                             update_response = await client.put(
136 |                                 f"{BLOG_SERVICE_URL}/blogs/{blog_id}/content",
137 |                                 json=content_data
138 |                             )
139 |                             
140 |                             if update_response.status_code == 200:
141 |                                 logger.info(f"WriterAgent: Updated blog {blog_id} with generated content")
142 |                             else:
143 |                                 logger.warning(f"WriterAgent: Failed to update blog content: {update_response.status_code}")
144 |                     else:
145 |                         logger.warning(f"WriterAgent: Failed to create blog: {create_response.status_code}")
146 |                         
147 |             except Exception as api_error:
148 |                 logger.error(f"WriterAgent: API call failed: {str(api_error)}")
149 |                 # Continue even if API call fails
150 |             
151 |             # Calculate processing time
152 |             end_time = datetime.utcnow()
153 |             processing_time_ms = int((end_time - start_time).total_seconds() * 1000)
154 |             
155 |             result_data = {
156 |                 "content": content,
157 |                 "word_count": len(content.split()),
158 |                 "char_count": len(content),
159 |                 "model": "ibm/granite-3-8b-instruct",
160 |                 "processing_time_ms": processing_time_ms
161 |             }
162 |             
163 |             if blog_created and blog_id:
164 |                 result_data["blog_id"] = blog_id
165 |                 result_data["blog_status"] = "draft"
166 |                 result_data["blog_title"] = title
167 |             
168 |             return AgentResult(
169 |                 success=True,
170 |                 data=result_data,
171 |                 metadata={
172 |                     "prompt": prompt,
173 |                     "tone": tone,
174 |                     "blog_created": blog_created
175 |                 }
176 |             )
177 |             
178 |         except Exception as e:
179 |             logger.error(f"WriterAgent: Failed to generate content: {str(e)}")
180 |             return AgentResult(
181 |                 success=False,
182 |                 error=str(e)
183 |             )
184 | 
185 | # Made with Bob
</content>
</file>
<file><path>services/ui_service/templates/agent_dashboard.html</path>
<content lines="1-395">
  1 | {% extends "base.html" %}
  2 | 
  3 | {% block title %}Agent Performance Dashboard{% endblock %}
  4 | 
  5 | {% block content %}
  6 | <div style="margin-bottom: 2rem;">
  7 |     <h2>🤖 Agent Performance Dashboard</h2>
  8 |     <p style="color: #666;">Real-time monitoring of agentic AI orchestration</p>
  9 | </div>
 10 | 
 11 | <!-- Metrics Overview -->
 12 | <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 1rem; margin-bottom: 2rem;">
 13 |     <div class="card" style="text-align: center; padding: 1.5rem;">
 14 |         <div style="font-size: 2rem; font-weight: bold; color: #3498db;" id="total-pipelines">0</div>
 15 |         <div style="color: #666; margin-top: 0.5rem;">Total Pipelines</div>
 16 |     </div>
 17 |     <div class="card" style="text-align: center; padding: 1.5rem;">
 18 |         <div style="font-size: 2rem; font-weight: bold; color: #2ecc71;" id="completed-pipelines">0</div>
 19 |         <div style="color: #666; margin-top: 0.5rem;">Completed</div>
 20 |     </div>
 21 |     <div class="card" style="text-align: center; padding: 1.5rem;">
 22 |         <div style="font-size: 2rem; font-weight: bold; color: #e74c3c;" id="failed-pipelines">0</div>
 23 |         <div style="color: #666; margin-top: 0.5rem;">Failed</div>
 24 |     </div>
 25 |     <div class="card" style="text-align: center; padding: 1.5rem;">
 26 |         <div style="font-size: 2rem; font-weight: bold; color: #f39c12;" id="running-pipelines">0</div>
 27 |         <div style="color: #666; margin-top: 0.5rem;">Running</div>
 28 |     </div>
 29 |     <div class="card" style="text-align: center; padding: 1.5rem;">
 30 |         <div style="font-size: 2rem; font-weight: bold; color: #9b59b6;" id="success-rate">0%</div>
 31 |         <div style="color: #666; margin-top: 0.5rem;">Success Rate</div>
 32 |     </div>
 33 |     <div class="card" style="text-align: center; padding: 1.5rem;">
 34 |         <div style="font-size: 2rem; font-weight: bold; color: #1abc9c;" id="avg-duration">0s</div>
 35 |         <div style="color: #666; margin-top: 0.5rem;">Avg Duration</div>
 36 |     </div>
 37 | </div>
 38 | 
 39 | <!-- Agent Runner -->
 40 | <div class="card" style="margin-bottom: 2rem;">
 41 |     <h3 style="margin-bottom: 1rem;">🚀 Run Individual Agents</h3>
 42 |     <p style="color: #666; margin-bottom: 1rem;">Execute agents independently with custom input</p>
 43 |     <div id="agent-runner" style="display: grid; gap: 1rem;">
 44 |         <!-- Agent cards will be populated here -->
 45 |     </div>
 46 | </div>
 47 | 
 48 | <!-- Agent Usage Statistics -->
 49 | <div class="card" style="margin-bottom: 2rem;">
 50 |     <h3 style="margin-bottom: 1rem;">Agent Usage Statistics</h3>
 51 |     <div id="agent-stats" style="display: grid; gap: 1rem;">
 52 |         <!-- Agent stats will be populated here -->
 53 |     </div>
 54 | </div>
 55 | 
 56 | <!-- Active Pipelines -->
 57 | <div class="card" style="margin-bottom: 2rem;">
 58 |     <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1rem;">
 59 |         <h3>Active Pipelines</h3>
 60 |         <button onclick="refreshDashboard()" class="btn" style="font-size: 0.9rem; padding: 0.5rem 1rem;">
 61 |             🔄 Refresh
 62 |         </button>
 63 |     </div>
 64 |     <div id="pipelines-list">
 65 |         <!-- Pipelines will be populated here -->
 66 |     </div>
 67 | </div>
 68 | 
 69 | <!-- Recent Pipeline Executions -->
 70 | <div class="card">
 71 |     <h3 style="margin-bottom: 1rem;">Recent Pipeline Executions</h3>
 72 |     <div id="recent-pipelines">
 73 |         <!-- Recent pipelines will be populated here -->
 74 |     </div>
 75 | </div>
 76 | 
 77 | <script>
 78 | // Auto-refresh every 3 seconds
 79 | let autoRefreshInterval;
 80 | 
 81 | async function fetchMetrics() {
 82 |     try {
 83 |         const response = await fetch('http://localhost:8004/metrics');
 84 |         const data = await response.json();
 85 |         return data.data;
 86 |     } catch (error) {
 87 |         console.error('Error fetching metrics:', error);
 88 |         return null;
 89 |     }
 90 | }
 91 | 
 92 | async function fetchPipelines() {
 93 |     try {
 94 |         const response = await fetch('http://localhost:8004/pipelines');
 95 |         const data = await response.json();
 96 |         return data.data;
 97 |     } catch (error) {
 98 |         console.error('Error fetching pipelines:', error);
 99 |         return null;
100 |     }
101 | }
102 | 
103 | async function fetchAgents() {
104 |     try {
105 |         const response = await fetch('http://localhost:8004/agents');
106 |         const data = await response.json();
107 |         return data.data;
108 |     } catch (error) {
109 |         console.error('Error fetching agents:', error);
110 |         return null;
111 |     }
112 | }
113 | 
114 | async function runAgent(agentName, inputData) {
115 |     try {
116 |         const response = await fetch(`http://localhost:8004/agents/${agentName}/run`, {
117 |             method: 'POST',
118 |             headers: {
119 |                 'Content-Type': 'application/json'
120 |             },
121 |             body: JSON.stringify(inputData)
122 |         });
123 |         const data = await response.json();
124 |         return data;
125 |     } catch (error) {
126 |         console.error('Error running agent:', error);
127 |         return { success: false, error: error.message };
128 |     }
129 | }
130 | 
131 | function showAgentInputModal(agentName, metadata) {
132 |     const modal = document.createElement('div');
133 |     modal.style.cssText = `
134 |         position: fixed;
135 |         top: 0;
136 |         left: 0;
137 |         right: 0;
138 |         bottom: 0;
139 |         background: rgba(0,0,0,0.5);
140 |         display: flex;
141 |         align-items: center;
142 |         justify-content: center;
143 |         z-index: 1000;
144 |     `;
145 |     
146 |     const inputFields = Object.entries(metadata.input_schema).map(([key, desc]) => `
147 |         <div style="margin-bottom: 1rem;">
148 |             <label style="display: block; margin-bottom: 0.5rem; font-weight: bold;">${key}</label>
149 |             <textarea
150 |                 id="input-${key}"
151 |                 placeholder="${desc}"
152 |                 style="width: 100%; padding: 0.5rem; border: 1px solid #ddd; border-radius: 4px; min-height: 60px;"
153 |             ></textarea>
154 |         </div>
155 |     `).join('');
156 |     
157 |     modal.innerHTML = `
158 |         <div style="background: white; padding: 2rem; border-radius: 8px; max-width: 600px; width: 90%; max-height: 80vh; overflow-y: auto;">
159 |             <h3 style="margin-bottom: 1rem;">Run ${metadata.display_name}</h3>
160 |             <p style="color: #666; margin-bottom: 1.5rem;">${metadata.description}</p>
161 |             
162 |             <form id="agent-form">
163 |                 ${inputFields}
164 |                 
165 |                 <div style="display: flex; gap: 1rem; margin-top: 1.5rem;">
166 |                     <button type="submit" class="btn" style="flex: 1;">
167 |                         ▶️ Run Agent
168 |                     </button>
169 |                     <button type="button" class="btn" onclick="this.closest('[style*=fixed]').remove()"
170 |                             style="flex: 1; background: #95a5a6;">
171 |                         Cancel
172 |                     </button>
173 |                 </div>
174 |             </form>
175 |             
176 |             <div id="agent-result" style="margin-top: 1.5rem; display: none;"></div>
177 |         </div>
178 |     `;
179 |     
180 |     document.body.appendChild(modal);
181 |     
182 |     document.getElementById('agent-form').addEventListener('submit', async (e) => {
183 |         e.preventDefault();
184 |         
185 |         const inputData = {};
186 |         Object.keys(metadata.input_schema).forEach(key => {
187 |             const value = document.getElementById(`input-${key}`).value;
188 |             if (value) inputData[key] = value;
189 |         });
190 |         
191 |         const resultDiv = document.getElementById('agent-result');
192 |         resultDiv.style.display = 'block';
193 |         resultDiv.innerHTML = '<p style="color: #f39c12;">⏳ Running agent...</p>';
194 |         
195 |         const result = await runAgent(agentName, inputData);
196 |         
197 |         if (result.success) {
198 |             resultDiv.innerHTML = `
199 |                 <div style="padding: 1rem; background: #d4edda; border: 1px solid #c3e6cb; border-radius: 4px;">
200 |                     <strong style="color: #155724;">✓ Success!</strong>
201 |                     <pre style="margin-top: 0.5rem; white-space: pre-wrap; font-size: 0.9rem;">${JSON.stringify(result.data, null, 2)}</pre>
202 |                 </div>
203 |                 <div style="display: flex; gap: 1rem; margin-top: 1rem;">
204 |                     <button type="button" class="btn" onclick="this.closest('[style*=fixed]').remove()"
205 |                             style="flex: 1; background: #2ecc71;">
206 |                         ✓ Close
207 |                     </button>
208 |                 </div>
209 |             `;
210 |         } else {
211 |             resultDiv.innerHTML = `
212 |                 <div style="padding: 1rem; background: #f8d7da; border: 1px solid #f5c6cb; border-radius: 4px;">
213 |                     <strong style="color: #721c24;">✗ Error</strong>
214 |                     <p style="margin-top: 0.5rem;">${result.error || result.detail || 'Unknown error'}</p>
215 |                 </div>
216 |                 <div style="display: flex; gap: 1rem; margin-top: 1rem;">
217 |                     <button type="button" class="btn" onclick="this.closest('[style*=fixed]').remove()"
218 |                             style="flex: 1; background: #95a5a6;">
219 |                         Close
220 |                     </button>
221 |                 </div>
222 |             `;
223 |         }
224 |     });
225 | }
226 | 
227 | function updateAgentRunner(agents) {
228 |     if (!agents || !agents.agent_metadata) return;
229 |     
230 |     const runnerDiv = document.getElementById('agent-runner');
231 |     runnerDiv.innerHTML = '';
232 |     
233 |     for (const [agentName, metadata] of Object.entries(agents.agent_metadata)) {
234 |         const agentCard = document.createElement('div');
235 |         agentCard.style.cssText = 'border: 1px solid #ddd; border-radius: 8px; padding: 1.5rem; cursor: pointer; transition: all 0.2s;';
236 |         agentCard.onmouseover = () => agentCard.style.borderColor = '#3498db';
237 |         agentCard.onmouseout = () => agentCard.style.borderColor = '#ddd';
238 |         
239 |         agentCard.innerHTML = `
240 |             <div style="display: flex; justify-content: space-between; align-items: start; margin-bottom: 0.5rem;">
241 |                 <div>
242 |                     <strong style="font-size: 1.1rem; color: #2c3e50; display: block;">${metadata.display_name}</strong>
243 |                     <span style="background: #3498db; color: white; padding: 0.2rem 0.6rem; border-radius: 12px; font-size: 0.75rem; display: inline-block; margin-top: 0.25rem;">
244 |                         ${agentName}
245 |                     </span>
246 |                 </div>
247 |                 <button style="background: #3498db; color: white; border: none; padding: 0.5rem 1rem; border-radius: 4px; cursor: pointer; font-size: 0.9rem;">
248 |                     ▶️ Run
249 |                 </button>
250 |             </div>
251 |             <p style="color: #666; margin-bottom: 1rem; line-height: 1.5;">${metadata.description}</p>
252 |             <div style="display: flex; gap: 0.5rem; flex-wrap: wrap;">
253 |                 ${Object.keys(metadata.input_schema).map(key =>
254 |                     `<span style="background: #ecf0f1; padding: 0.25rem 0.5rem; border-radius: 4px; font-size: 0.85rem;">📝 ${key}</span>`
255 |                 ).join('')}
256 |             </div>
257 |         `;
258 |         
259 |         agentCard.onclick = () => showAgentInputModal(agentName, metadata);
260 |         runnerDiv.appendChild(agentCard);
261 |     }
262 | }
263 | 
264 | function updateMetrics(metrics) {
265 |     if (!metrics) return;
266 |     
267 |     document.getElementById('total-pipelines').textContent = metrics.total_pipelines;
268 |     document.getElementById('completed-pipelines').textContent = metrics.completed;
269 |     document.getElementById('failed-pipelines').textContent = metrics.failed;
270 |     document.getElementById('running-pipelines').textContent = metrics.running;
271 |     document.getElementById('success-rate').textContent = metrics.success_rate.toFixed(1) + '%';
272 |     document.getElementById('avg-duration').textContent = metrics.avg_duration_seconds.toFixed(1) + 's';
273 |     
274 |     // Update agent stats
275 |     const agentStatsDiv = document.getElementById('agent-stats');
276 |     agentStatsDiv.innerHTML = '';
277 |     
278 |     for (const [agentName, stats] of Object.entries(metrics.agent_usage)) {
279 |         const successRate = stats.total > 0 ? (stats.success / stats.total * 100).toFixed(1) : 0;
280 |         const agentCard = `
281 |             <div style="border: 1px solid #ddd; border-radius: 8px; padding: 1rem;">
282 |                 <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.5rem;">
283 |                     <strong style="text-transform: capitalize;">${agentName} Agent</strong>
284 |                     <span style="background: #3498db; color: white; padding: 0.25rem 0.5rem; border-radius: 4px; font-size: 0.8rem;">
285 |                         ${successRate}% success
286 |                     </span>
287 |                 </div>
288 |                 <div style="display: flex; gap: 1rem; font-size: 0.9rem; color: #666;">
289 |                     <span>Total: ${stats.total}</span>
290 |                     <span style="color: #2ecc71;">✓ ${stats.success}</span>
291 |                     <span style="color: #e74c3c;">✗ ${stats.failed}</span>
292 |                 </div>
293 |             </div>
294 |         `;
295 |         agentStatsDiv.innerHTML += agentCard;
296 |     }
297 | }
298 | 
299 | function updatePipelines(pipelines) {
300 |     if (!pipelines) return;
301 |     
302 |     const pipelinesDiv = document.getElementById('pipelines-list');
303 |     const recentDiv = document.getElementById('recent-pipelines');
304 |     
305 |     const pipelineArray = Object.entries(pipelines);
306 |     
307 |     if (pipelineArray.length === 0) {
308 |         pipelinesDiv.innerHTML = '<p style="color: #666; text-align: center; padding: 2rem;">No pipelines yet</p>';
309 |         recentDiv.innerHTML = '<p style="color: #666; text-align: center; padding: 2rem;">No recent executions</p>';
310 |         return;
311 |     }
312 |     
313 |     // Show running pipelines
314 |     const runningPipelines = pipelineArray.filter(([_, p]) => p.state === 'running');
315 |     if (runningPipelines.length > 0) {
316 |         pipelinesDiv.innerHTML = runningPipelines.map(([id, pipeline]) => {
317 |             const progress = pipeline.total_steps > 0 ? 
318 |                 ((pipeline.current_step + 1) / pipeline.total_steps * 100).toFixed(0) : 0;
319 |             
320 |             return `
321 |                 <div style="border: 1px solid #f39c12; border-radius: 8px; padding: 1rem; margin-bottom: 1rem; background: #fff9e6;">
322 |                     <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.5rem;">
323 |                         <strong>${pipeline.name}</strong>
324 |                         <span style="background: #f39c12; color: white; padding: 0.25rem 0.5rem; border-radius: 4px; font-size: 0.8rem;">
325 |                             RUNNING
326 |                         </span>
327 |                     </div>
328 |                     <div style="margin-bottom: 0.5rem;">
329 |                         <div style="background: #ecf0f1; height: 8px; border-radius: 4px; overflow: hidden;">
330 |                             <div style="background: #f39c12; height: 100%; width: ${progress}%; transition: width 0.3s;"></div>
331 |                         </div>
332 |                     </div>
333 |                     <div style="font-size: 0.9rem; color: #666;">
334 |                         Step ${pipeline.current_step + 1} of ${pipeline.total_steps} • ${progress}% complete
335 |                     </div>
336 |                 </div>
337 |             `;
338 |         }).join('');
339 |     } else {
340 |         pipelinesDiv.innerHTML = '<p style="color: #666; text-align: center; padding: 1rem;">No active pipelines</p>';
341 |     }
342 |     
343 |     // Show recent completed/failed pipelines
344 |     const recentPipelines = pipelineArray
345 |         .filter(([_, p]) => p.state === 'completed' || p.state === 'failed')
346 |         .slice(0, 5);
347 |     
348 |     if (recentPipelines.length > 0) {
349 |         recentDiv.innerHTML = recentPipelines.map(([id, pipeline]) => {
350 |             const stateColor = pipeline.state === 'completed' ? '#2ecc71' : '#e74c3c';
351 |             const stateText = pipeline.state === 'completed' ? 'COMPLETED' : 'FAILED';
352 |             
353 |             return `
354 |                 <div style="border: 1px solid ${stateColor}; border-radius: 8px; padding: 1rem; margin-bottom: 1rem;">
355 |                     <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.5rem;">
356 |                         <strong>${pipeline.name}</strong>
357 |                         <span style="background: ${stateColor}; color: white; padding: 0.25rem 0.5rem; border-radius: 4px; font-size: 0.8rem;">
358 |                             ${stateText}
359 |                         </span>
360 |                     </div>
361 |                     <div style="font-size: 0.9rem; color: #666;">
362 |                         ${pipeline.total_steps} steps • ${pipeline.duration_seconds ? pipeline.duration_seconds.toFixed(2) + 's' : 'N/A'}
363 |                     </div>
364 |                 </div>
365 |             `;
366 |         }).join('');
367 |     } else {
368 |         recentDiv.innerHTML = '<p style="color: #666; text-align: center; padding: 1rem;">No recent executions</p>';
369 |     }
370 | }
371 | 
372 | async function refreshDashboard() {
373 |     const metrics = await fetchMetrics();
374 |     const pipelines = await fetchPipelines();
375 |     const agents = await fetchAgents();
376 |     
377 |     updateMetrics(metrics);
378 |     updatePipelines(pipelines);
379 |     updateAgentRunner(agents);
380 | }
381 | 
382 | // Initial load
383 | refreshDashboard();
384 | 
385 | // Auto-refresh every 3 seconds
386 | autoRefreshInterval = setInterval(refreshDashboard, 3000);
387 | 
388 | // Cleanup on page unload
389 | window.addEventListener('beforeunload', () => {
390 |     if (autoRefreshInterval) {
391 |         clearInterval(autoRefreshInterval);
392 |     }
393 | });
394 | </script>
395 | {% endblock %}
</content>
</file>
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
<file><path>services/orchestration_service/pipeline_manager.py</path>
<content lines="1-242">
  1 | """
  2 | Pipeline manager for orchestrating agent workflows
  3 | """
  4 | from typing import List, Dict, Any, Optional
  5 | from .agent_base import BaseAgent, AgentResult, AgentState
  6 | from .agent_registry import agent_registry
  7 | import logging
  8 | import uuid
  9 | from datetime import datetime
 10 | import asyncio
 11 | 
 12 | logger = logging.getLogger(__name__)
 13 | 
 14 | 
 15 | class PipelineStep:
 16 |     """Single step in a pipeline"""
 17 |     
 18 |     def __init__(
 19 |         self,
 20 |         agent_name: str,
 21 |         input_mapping: Optional[Dict[str, str]] = None,
 22 |         condition: Optional[str] = None
 23 |     ):
 24 |         self.agent_name = agent_name
 25 |         self.input_mapping = input_mapping or {}
 26 |         self.condition = condition  # For conditional execution
 27 |         self.agent_id: Optional[str] = None
 28 |         self.result: Optional[AgentResult] = None
 29 | 
 30 | 
 31 | class Pipeline:
 32 |     """Agent execution pipeline"""
 33 |     
 34 |     def __init__(self, pipeline_id: Optional[str] = None, name: str = "Unnamed Pipeline"):
 35 |         self.pipeline_id = pipeline_id or str(uuid.uuid4())
 36 |         self.name = name
 37 |         self.steps: List[PipelineStep] = []
 38 |         self.state = "idle"
 39 |         self.current_step = 0
 40 |         self.context: Dict[str, Any] = {}
 41 |         self.start_time: Optional[datetime] = None
 42 |         self.end_time: Optional[datetime] = None
 43 |         logger.info(f"Pipeline created: {name} ({self.pipeline_id})")
 44 |     
 45 |     def add_step(
 46 |         self,
 47 |         agent_name: str,
 48 |         input_mapping: Optional[Dict[str, str]] = None,
 49 |         condition: Optional[str] = None
 50 |     ):
 51 |         """Add a step to the pipeline"""
 52 |         step = PipelineStep(agent_name, input_mapping, condition)
 53 |         self.steps.append(step)
 54 |         logger.info(f"Added step to pipeline {self.name}: {agent_name}")
 55 |     
 56 |     async def execute(self, initial_input: Dict[str, Any]) -> Dict[str, Any]:
 57 |         """
 58 |         Execute the pipeline
 59 |         
 60 |         Args:
 61 |             initial_input: Initial input data
 62 |             
 63 |         Returns:
 64 |             Pipeline execution result
 65 |         """
 66 |         self.state = "running"
 67 |         self.start_time = datetime.utcnow()
 68 |         self.context = {"initial_input": initial_input}
 69 |         
 70 |         logger.info(f"Starting pipeline execution: {self.name}")
 71 |         
 72 |         try:
 73 |             for i, step in enumerate(self.steps):
 74 |                 self.current_step = i
 75 |                 logger.info(f"Pipeline {self.name}: Executing step {i+1}/{len(self.steps)} - {step.agent_name}")
 76 |                 
 77 |                 # Create agent instance
 78 |                 agent = agent_registry.create_agent(step.agent_name)
 79 |                 step.agent_id = agent.agent_id
 80 |                 
 81 |                 # Prepare input data
 82 |                 if i == 0:
 83 |                     # First step uses initial input
 84 |                     input_data = initial_input
 85 |                 else:
 86 |                     # Subsequent steps use previous step's output
 87 |                     prev_result = self.steps[i-1].result
 88 |                     if prev_result and prev_result.success:
 89 |                         input_data = prev_result.data
 90 |                     else:
 91 |                         raise Exception(f"Previous step failed: {step.agent_name}")
 92 |                 
 93 |                 # Apply input mapping if specified
 94 |                 if step.input_mapping:
 95 |                     mapped_input = {}
 96 |                     for target_key, source_key in step.input_mapping.items():
 97 |                         if source_key in input_data:
 98 |                             mapped_input[target_key] = input_data[source_key]
 99 |                     input_data = mapped_input
100 |                 
101 |                 # Execute agent
102 |                 result = await agent.run(input_data)
103 |                 step.result = result
104 |                 
105 |                 # Store result in context
106 |                 self.context[f"step_{i}_{step.agent_name}"] = result.to_dict()
107 |                 
108 |                 # Check if step failed
109 |                 if not result.success:
110 |                     logger.error(f"Pipeline {self.name}: Step {i+1} failed - {step.agent_name}")
111 |                     self.state = "failed"
112 |                     break
113 |                 
114 |                 logger.info(f"Pipeline {self.name}: Step {i+1} completed successfully")
115 |             
116 |             # Pipeline completed
117 |             if self.state != "failed":
118 |                 self.state = "completed"
119 |                 logger.info(f"Pipeline {self.name}: Execution completed successfully")
120 |             
121 |         except Exception as e:
122 |             logger.error(f"Pipeline {self.name}: Execution failed: {str(e)}")
123 |             self.state = "failed"
124 |             self.context["error"] = str(e)
125 |         
126 |         finally:
127 |             self.end_time = datetime.utcnow()
128 |             duration = (self.end_time - self.start_time).total_seconds()
129 |             self.context["duration_seconds"] = duration
130 |         
131 |         return self.get_status()
132 |     
133 |     def get_status(self) -> Dict[str, Any]:
134 |         """Get pipeline status"""
135 |         return {
136 |             "pipeline_id": self.pipeline_id,
137 |             "name": self.name,
138 |             "state": self.state,
139 |             "current_step": self.current_step,
140 |             "total_steps": len(self.steps),
141 |             "steps": [
142 |                 {
143 |                     "agent_name": step.agent_name,
144 |                     "agent_id": step.agent_id,
145 |                     "completed": step.result is not None,
146 |                     "success": step.result.success if step.result else None
147 |                 }
148 |                 for step in self.steps
149 |             ],
150 |             "start_time": self.start_time.isoformat() if self.start_time else None,
151 |             "end_time": self.end_time.isoformat() if self.end_time else None,
152 |             "duration_seconds": self.context.get("duration_seconds")
153 |         }
154 | 
155 | 
156 | class PipelineManager:
157 |     """Manager for creating and executing pipelines"""
158 |     
159 |     def __init__(self):
160 |         self._pipelines: Dict[str, Pipeline] = {}
161 |         logger.info("Pipeline manager initialized")
162 |     
163 |     @property
164 |     def pipelines(self) -> Dict[str, Pipeline]:
165 |         """Get all pipelines"""
166 |         return self._pipelines
167 |     
168 |     def create_pipeline(self, name: str) -> Pipeline:
169 |         """Create a new pipeline"""
170 |         pipeline = Pipeline(name=name)
171 |         self._pipelines[pipeline.pipeline_id] = pipeline
172 |         return pipeline
173 |     
174 |     def get_pipeline(self, pipeline_id: str) -> Optional[Pipeline]:
175 |         """Get pipeline by ID"""
176 |         return self._pipelines.get(pipeline_id)
177 |     
178 |     def list_pipelines(self) -> Dict[str, Dict]:
179 |         """List all pipelines"""
180 |         return {
181 |             pipeline_id: pipeline.get_status()
182 |             for pipeline_id, pipeline in self._pipelines.items()
183 |         }
184 |     
185 |     async def execute_pipeline(
186 |         self,
187 |         pipeline_id: str,
188 |         initial_input: Dict[str, Any]
189 |     ) -> Dict[str, Any]:
190 |         """Execute a pipeline"""
191 |         pipeline = self.get_pipeline(pipeline_id)
192 |         if not pipeline:
193 |             raise ValueError(f"Pipeline not found: {pipeline_id}")
194 |         
195 |         return await pipeline.execute(initial_input)
196 |     
197 |     def get_metrics(self) -> Dict[str, Any]:
198 |         """Get aggregated metrics across all pipelines"""
199 |         total_pipelines = len(self.pipelines)
200 |         completed = sum(1 for p in self.pipelines.values() if p.state == "completed")
201 |         failed = sum(1 for p in self.pipelines.values() if p.state == "failed")
202 |         running = sum(1 for p in self.pipelines.values() if p.state == "running")
203 |         
204 |         # Calculate average duration for completed pipelines
205 |         durations = []
206 |         for pipeline in self.pipelines.values():
207 |             if pipeline.state == "completed" and pipeline.start_time and pipeline.end_time:
208 |                 duration = (pipeline.end_time - pipeline.start_time).total_seconds()
209 |                 durations.append(duration)
210 |         
211 |         avg_duration = sum(durations) / len(durations) if durations else 0
212 |         
213 |         # Agent usage statistics
214 |         agent_usage = {}
215 |         for pipeline in self.pipelines.values():
216 |             for step in pipeline.steps:
217 |                 agent_name = step.agent_name
218 |                 if agent_name not in agent_usage:
219 |                     agent_usage[agent_name] = {"total": 0, "success": 0, "failed": 0}
220 |                 
221 |                 agent_usage[agent_name]["total"] += 1
222 |                 if step.result:
223 |                     if step.result.success:
224 |                         agent_usage[agent_name]["success"] += 1
225 |                     else:
226 |                         agent_usage[agent_name]["failed"] += 1
227 |         
228 |         return {
229 |             "total_pipelines": total_pipelines,
230 |             "completed": completed,
231 |             "failed": failed,
232 |             "running": running,
233 |             "success_rate": (completed / total_pipelines * 100) if total_pipelines > 0 else 0,
234 |             "avg_duration_seconds": round(avg_duration, 2),
235 |             "agent_usage": agent_usage
236 |         }
237 | 
238 | 
239 | # Global pipeline manager instance
240 | pipeline_manager = PipelineManager()
241 | 
242 | # Made with Bob
</content>
</file>
</files>
<environment_details>
# VSCode Visible Files


# VSCode Open Tabs
.vscode/settings.json,services/ui_service/templates/home.html,.bobalytics.json,.gitignore,services/orchestration_service/agent_base.py,services/orchestration_service/agents/publisher_agent.py,services/orchestration_service/agent_registry.py,stop_all_services.py,services/ui_service/main.py,services/orchestration_service/main.py,services/ui_service/templates/agent_dashboard.html,services/orchestration_service/agents/writer_agent.py,services/orchestration_service/pipeline_manager.py,test_agent_metadata.py,test_orchestration.py,enhancement1_B_delta_agent_dashboard.md,services/ui_service/templates/base.html,services/ui_service/templates/create.html,services/api_gateway/main.py,services/orchestration_service/agents/__init__.py

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

# Current Time
Current time in ISO 8601 UTC format: 2026-05-02T08:12:11.501Z
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

I can see the issues! Let me create a todo list and fix them step by step.

<update_todo_list>
<todos>
[ ] Fix writer agent manual run - blog not being saved to Home
[ ] Fix API calls not showing in API logs
[ ] Test the fixes
</todos>
</update_todo_list>

Now let me examine the orchestration service main.py to understand the agent run endpoint:

<read_file>
<args>
<file>
<path>services/orchestration_service/main.py</path>
</file>
</args>
</read_file>

---

**User:**

[update_todo_list] Result:
Todo list updated successfully.
Tool [read_file] was not executed because a tool has already been used in this message. Only one tool may be used per message. You must assess the first tool's result before proceeding to use the next tool.
<environment_details>
# VSCode Visible Files


# VSCode Open Tabs
.vscode/settings.json,services/ui_service/templates/home.html,.bobalytics.json,.gitignore,services/orchestration_service/agent_base.py,services/orchestration_service/agents/publisher_agent.py,services/orchestration_service/agent_registry.py,stop_all_services.py,services/ui_service/main.py,services/orchestration_service/main.py,services/ui_service/templates/agent_dashboard.html,services/orchestration_service/agents/writer_agent.py,services/orchestration_service/pipeline_manager.py,test_agent_metadata.py,test_orchestration.py,enhancement1_B_delta_agent_dashboard.md,services/ui_service/templates/base.html,services/ui_service/templates/create.html,services/api_gateway/main.py,services/orchestration_service/agents/__init__.py

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

# Current Time
Current time in ISO 8601 UTC format: 2026-05-02T08:12:29.106Z
User time zone: America/New_York, UTC-4:00

# Current Cost
$0.10

# Review Exclusions
The following file patterns are excluded from code reviews:
- .vscode/**

# Current Mode
<slug>code</slug>
<name>💻 Code</name>
====

REMINDERS

Below is your current list of reminders for this task. Keep them updated as you progress.

| # | Content | Status |
|---|---------|--------|
| 1 | Fix writer agent manual run - blog not being saved to Home | Pending |
| 2 | Fix API calls not showing in API logs | Pending |
| 3 | Test the fixes | Pending |


IMPORTANT: When task status changes, remember to call the `update_todo_list` tool to update your progress.

</environment_details>

---

**Assistant:**

<read_file>
<args>
<file>
<path>services/orchestration_service/main.py</path>
</file>
</args>
</read_file>

---

**User:**

[read_file for 'services/orchestration_service/main.py'. Reading multiple files at once is more efficient for the LLM. If other files are relevant to your current task, please read them simultaneously.] Result:
<files>
<file><path>services/orchestration_service/main.py</path>
<content lines="1-238">
  1 | """
  2 | Orchestration Service - Manages agent pipelines
  3 | """
  4 | from fastapi import FastAPI, HTTPException, BackgroundTasks
  5 | from fastapi.middleware.cors import CORSMiddleware
  6 | from pydantic import BaseModel
  7 | from typing import Dict, Any, Optional
  8 | import logging
  9 | 
 10 | from .agent_registry import agent_registry
 11 | from .pipeline_manager import pipeline_manager
 12 | from .agents import WriterAgent, PublisherAgent
 13 | 
 14 | # Configure logging
 15 | logging.basicConfig(level=logging.INFO)
 16 | logger = logging.getLogger(__name__)
 17 | 
 18 | app = FastAPI(
 19 |     title="Orchestration Service",
 20 |     description="Agent orchestration and pipeline management",
 21 |     version="1.0.0"
 22 | )
 23 | 
 24 | # Configure CORS
 25 | app.add_middleware(
 26 |     CORSMiddleware,
 27 |     allow_origins=[
 28 |         "http://localhost:8003",  # UI Service
 29 |         "http://127.0.0.1:8003",
 30 |         "http://localhost:8000",  # API Gateway
 31 |         "http://127.0.0.1:8000",
 32 |     ],
 33 |     allow_credentials=True,
 34 |     allow_methods=["*"],
 35 |     allow_headers=["*"],
 36 | )
 37 | 
 38 | 
 39 | # Request models
 40 | class PipelineRequest(BaseModel):
 41 |     name: str
 42 |     steps: list[Dict[str, Any]]
 43 | 
 44 | 
 45 | class ExecutionRequest(BaseModel):
 46 |     pipeline_id: str
 47 |     input_data: Dict[str, Any]
 48 | 
 49 | 
 50 | class BlogGenerationRequest(BaseModel):
 51 |     prompt: str
 52 |     blog_id: Optional[str] = None
 53 |     tone: Optional[str] = "professional"
 54 | 
 55 | 
 56 | # Initialize agents
 57 | @app.on_event("startup")
 58 | async def startup_event():
 59 |     """Register agents on startup"""
 60 |     logger.info("Registering agents...")
 61 |     agent_registry.register_agent_class("writer", WriterAgent)
 62 |     agent_registry.register_agent_class("publisher", PublisherAgent)
 63 |     logger.info("Agents registered successfully")
 64 | 
 65 | 
 66 | @app.get("/")
 67 | async def root():
 68 |     """Root endpoint"""
 69 |     return {
 70 |         "service": "Orchestration Service",
 71 |         "version": "1.0.0",
 72 |         "status": "active"
 73 |     }
 74 | 
 75 | 
 76 | @app.get("/health")
 77 | async def health_check():
 78 |     """Health check endpoint"""
 79 |     return {"status": "healthy"}
 80 | 
 81 | 
 82 | @app.get("/agents")
 83 | async def list_agents():
 84 |     """List all registered agents"""
 85 |     return {
 86 |         "success": True,
 87 |         "data": {
 88 |             "agent_classes": agent_registry.list_agent_classes(),
 89 |             "agent_instances": agent_registry.list_agents(),
 90 |             "agent_metadata": agent_registry.get_agent_metadata()
 91 |         }
 92 |     }
 93 | 
 94 | 
 95 | @app.post("/agents/{agent_name}/run")
 96 | async def run_agent(agent_name: str, input_data: Dict[str, Any]):
 97 |     """
 98 |     Run a single agent with provided input
 99 |     
100 |     Args:
101 |         agent_name: Name of the agent to run (e.g., "writer", "publisher")
102 |         input_data: Input data for the agent
103 |     
104 |     Returns:
105 |         Agent execution result
106 |     """
107 |     try:
108 |         # Create agent instance
109 |         agent = agent_registry.create_agent(agent_name)
110 |         
111 |         # Run agent
112 |         result = await agent.run(input_data)
113 |         
114 |         return {
115 |             "success": True,
116 |             "message": f"{agent_name} agent executed successfully",
117 |             "data": result.to_dict()
118 |         }
119 |         
120 |     except ValueError as e:
121 |         raise HTTPException(status_code=404, detail=str(e))
122 |     except Exception as e:
123 |         logger.error(f"Failed to run agent {agent_name}: {str(e)}")
124 |         raise HTTPException(status_code=500, detail=str(e))
125 | 
126 | 
127 | @app.get("/metrics")
128 | async def get_metrics():
129 |     """Get orchestration metrics"""
130 |     return {
131 |         "success": True,
132 |         "data": pipeline_manager.get_metrics()
133 |     }
134 | 
135 | 
136 | @app.post("/pipelines")
137 | async def create_pipeline(request: PipelineRequest):
138 |     """Create a new pipeline"""
139 |     try:
140 |         pipeline = pipeline_manager.create_pipeline(request.name)
141 |         
142 |         for step in request.steps:
143 |             pipeline.add_step(
144 |                 agent_name=step["agent_name"],
145 |                 input_mapping=step.get("input_mapping"),
146 |                 condition=step.get("condition")
147 |             )
148 |         
149 |         return {
150 |             "success": True,
151 |             "data": {
152 |                 "pipeline_id": pipeline.pipeline_id,
153 |                 "name": pipeline.name,
154 |                 "steps": len(pipeline.steps)
155 |             }
156 |         }
157 |     except Exception as e:
158 |         raise HTTPException(status_code=500, detail=str(e))
159 | 
160 | 
161 | @app.get("/pipelines")
162 | async def list_pipelines():
163 |     """List all pipelines"""
164 |     return {
165 |         "success": True,
166 |         "data": pipeline_manager.list_pipelines()
167 |     }
168 | 
169 | 
170 | @app.get("/pipelines/{pipeline_id}")
171 | async def get_pipeline_status(pipeline_id: str):
172 |     """Get pipeline status"""
173 |     pipeline = pipeline_manager.get_pipeline(pipeline_id)
174 |     if not pipeline:
175 |         raise HTTPException(status_code=404, detail="Pipeline not found")
176 |     
177 |     return {
178 |         "success": True,
179 |         "data": pipeline.get_status()
180 |     }
181 | 
182 | 
183 | @app.post("/pipelines/{pipeline_id}/execute")
184 | async def execute_pipeline(pipeline_id: str, request: ExecutionRequest):
185 |     """Execute a pipeline"""
186 |     try:
187 |         result = await pipeline_manager.execute_pipeline(
188 |             pipeline_id=request.pipeline_id,
189 |             initial_input=request.input_data
190 |         )
191 |         
192 |         return {
193 |             "success": True,
194 |             "data": result
195 |         }
196 |     except Exception as e:
197 |         raise HTTPException(status_code=500, detail=str(e))
198 | 
199 | 
200 | @app.post("/blog/generate")
201 | async def generate_blog(request: BlogGenerationRequest):
202 |     """
203 |     Generate blog using Writer → Publisher pipeline
204 |     
205 |     This is a convenience endpoint that creates and executes
206 |     a simple 2-agent pipeline.
207 |     """
208 |     try:
209 |         # Create pipeline
210 |         pipeline = pipeline_manager.create_pipeline("Blog Generation Pipeline")
211 |         pipeline.add_step("writer")
212 |         pipeline.add_step("publisher")
213 |         
214 |         # Execute pipeline
215 |         input_data = {
216 |             "prompt": request.prompt,
217 |             "blog_id": request.blog_id,
218 |             "tone": request.tone
219 |         }
220 |         
221 |         result = await pipeline.execute(input_data)
222 |         
223 |         return {
224 |             "success": True,
225 |             "message": "Blog generated successfully",
226 |             "data": result
227 |         }
228 |         
229 |     except Exception as e:
230 |         logger.error(f"Blog generation failed: {str(e)}")
231 |         raise HTTPException(status_code=500, detail=str(e))
232 | 
233 | 
234 | if __name__ == "__main__":
235 |     import uvicorn
236 |     uvicorn.run(app, host="0.0.0.0", port=8004)
237 | 
238 | # Made with Bob
</content>
</file>
</files>
<environment_details>
# VSCode Visible Files


# VSCode Open Tabs
.vscode/settings.json,services/ui_service/templates/home.html,.bobalytics.json,.gitignore,services/orchestration_service/agent_base.py,services/orchestration_service/agents/publisher_agent.py,services/orchestration_service/agent_registry.py,stop_all_services.py,services/ui_service/main.py,services/orchestration_service/main.py,services/ui_service/templates/agent_dashboard.html,services/orchestration_service/agents/writer_agent.py,services/orchestration_service/pipeline_manager.py,test_agent_metadata.py,test_orchestration.py,enhancement1_B_delta_agent_dashboard.md,services/ui_service/templates/base.html,services/ui_service/templates/create.html,services/api_gateway/main.py,services/orchestration_service/agents/__init__.py

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

# Current Time
Current time in ISO 8601 UTC format: 2026-05-02T08:12:37.961Z
User time zone: America/New_York, UTC-4:00

# Current Cost
$0.18

# Review Exclusions
The following file patterns are excluded from code reviews:
- .vscode/**

# Current Mode
<slug>code</slug>
<name>💻 Code</name>
====

REMINDERS

Below is your current list of reminders for this task. Keep them updated as you progress.

| # | Content | Status |
|---|---------|--------|
| 1 | Fix writer agent manual run - blog not being saved to Home | Pending |
| 2 | Fix API calls not showing in API logs | Pending |
| 3 | Test the fixes | Pending |


IMPORTANT: When task status changes, remember to call the `update_todo_list` tool to update your progress.

</environment_details>

---

**Assistant:**

Now I understand the issues! Let me analyze:

**Issue 1**: When running the writer agent manually from the dashboard, the blog is created but not visible on the Home page because the Home page only shows blogs from `blogs_db`, and the writer agent creates blogs directly via API but they might not be persisting correctly.

**Issue 2**: The writer agent is logging to WatsonX logs, but the logs are being saved in the blog service, not being displayed because the writer agent is calling the blog service API directly without going through proper logging.

Let me check the home.html to see how blogs are loaded:

<read_file>
<args>
<file>
<path>services/ui_service/templates/home.html</path>
</file>
<file>
<path>services/ui_service/main.py</path>
</file>
</args>
</read_file>

---

**User:**

[read_file for 'services/ui_service/templates/home.html', 'services/ui_service/main.py'] Result:
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
</files>
<environment_details>
# VSCode Visible Files


# VSCode Open Tabs
.vscode/settings.json,services/ui_service/templates/home.html,.bobalytics.json,.gitignore,services/orchestration_service/agent_base.py,services/orchestration_service/agents/publisher_agent.py,services/orchestration_service/agent_registry.py,stop_all_services.py,services/ui_service/main.py,services/orchestration_service/main.py,services/ui_service/templates/agent_dashboard.html,services/orchestration_service/agents/writer_agent.py,services/orchestration_service/pipeline_manager.py,test_agent_metadata.py,test_orchestration.py,enhancement1_B_delta_agent_dashboard.md,services/ui_service/templates/base.html,services/ui_service/templates/create.html,services/api_gateway/main.py,services/orchestration_service/agents/__init__.py

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

# Current Time
Current time in ISO 8601 UTC format: 2026-05-02T08:12:50.572Z
User time zone: America/New_York, UTC-4:00

# Current Cost
$0.28

# Review Exclusions
The following file patterns are excluded from code reviews:
- .vscode/**

# Current Mode
<slug>code</slug>
<name>💻 Code</name>
====

REMINDERS

Below is your current list of reminders for this task. Keep them updated as you progress.

| # | Content | Status |
|---|---------|--------|
| 1 | Fix writer agent manual run - blog not being saved to Home | Pending |
| 2 | Fix API calls not showing in API logs | Pending |
| 3 | Test the fixes | Pending |


IMPORTANT: When task status changes, remember to call the `update_todo_list` tool to update your progress.

</environment_details>

---

**Assistant:**

Perfect! Now I understand both issues:

**Issue 1**: The writer agent creates a blog via API and saves it, but the blog IS being saved. The issue is that the blogs ARE showing up on the home page - the home page fetches from `/api/blogs` which gets data from the blog service.

**Issue 2**: The writer agent is NOT logging API calls to WatsonX logs because it's using the Granite client directly without going through the blog service's logging mechanism.

Let me fix the writer agent to properly log API calls:

<apply_diff>
<path>services/orchestration_service/agents/writer_agent.py</path>
<diff>
<<<<<<< SEARCH
:start_line:1
-------
"""
Writer Agent - Generates blog content using Granite
"""
from ..agent_base import BaseAgent, AgentResult
from services.watsonx_service.granite_client import get_granite_client
from typing import Dict, Any
import logging
import httpx
from datetime import datetime

logger = logging.getLogger(__name__)

# Blog service URL
BLOG_SERVICE_URL = "http://localhost:8001"
=======
"""
Writer Agent - Generates blog content using Granite
"""
from ..agent_base import BaseAgent, AgentResult
from services.watsonx_service.granite_client import get_granite_client
from typing import Dict, Any
import logging
import httpx
from datetime import datetime

logger = logging.getLogger(__name__)

# Service URLs
BLOG_SERVICE_URL = "http://localhost:8001"
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
.vscode/settings.json,services/ui_service/templates/home.html,.bobalytics.json,.gitignore,services/orchestration_service/agent_base.py,services/orchestration_service/agents/publisher_agent.py,services/orchestration_service/agent_registry.py,services/orchestration_service/agents/writer_agent.py,stop_all_services.py,services/ui_service/main.py,services/orchestration_service/main.py,services/ui_service/templates/agent_dashboard.html,services/orchestration_service/pipeline_manager.py,test_agent_metadata.py,test_orchestration.py,enhancement1_B_delta_agent_dashboard.md,services/ui_service/templates/base.html,services/ui_service/templates/create.html,services/api_gateway/main.py,services/orchestration_service/agents/__init__.py

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

# Current Time
Current time in ISO 8601 UTC format: 2026-05-02T08:13:07.360Z
User time zone: America/New_York, UTC-4:00

# Current Cost
$0.40

# Review Exclusions
The following file patterns are excluded from code reviews:
- .vscode/**

# Current Mode
<slug>code</slug>
<name>💻 Code</name>
====

REMINDERS

Below is your current list of reminders for this task. Keep them updated as you progress.

| # | Content | Status |
|---|---------|--------|
| 1 | Fix writer agent manual run - blog not being saved to Home | Pending |
| 2 | Fix API calls not showing in API logs | Pending |
| 3 | Test the fixes | Pending |


IMPORTANT: When task status changes, remember to call the `update_todo_list` tool to update your progress.

</environment_details>

---

**Assistant:**

Now let me make the comprehensive fix to the writer agent to properly log API calls and ensure blogs are saved correctly:

<apply_diff>
<path>services/orchestration_service/agents/writer_agent.py</path>
<diff>
<<<<<<< SEARCH
:start_line:61
-------
        start_time = datetime.utcnow()
        
        try:
            prompt = input_data.get("prompt", "")
            research_brief = input_data.get("research_brief", "")
            tone = input_data.get("tone", "professional")
            
            if not prompt:
                return AgentResult(
                    success=False,
                    error="No prompt provided"
                )
            
            # Construct full prompt
            full_prompt = f"Topic: {prompt}\n\n"
            
            if research_brief:
                full_prompt += f"Research Context:\n{research_brief}\n\n"
            
            full_prompt += f"Tone: {tone}\n\n"
            full_prompt += "Write a complete blog post with title, introduction, body, and conclusion."
            
            logger.info(f"WriterAgent: Generating content for prompt: {prompt[:50]}...")
            
            # Generate content
            content = self.granite.generate(
                prompt=full_prompt,
                system_prompt=self.system_prompt,
                max_tokens=2048,
                temperature=0.7
            )
            
            logger.info(f"WriterAgent: Generated {len(content)} characters")
=======
        start_time = datetime.utcnow()
        
        try:
            prompt = input_data.get("prompt", "")
            research_brief = input_data.get("research_brief", "")
            tone = input_data.get("tone", "professional")
            
            if not prompt:
                return AgentResult(
                    success=False,
                    error="No prompt provided"
                )
            
            # Construct full prompt
            full_prompt = f"Topic: {prompt}\n\n"
            
            if research_brief:
                full_prompt += f"Research Context:\n{research_brief}\n\n"
            
            full_prompt += f"Tone: {tone}\n\n"
            full_prompt += "Write a complete blog post with title, introduction, body, and conclusion."
            
            logger.info(f"WriterAgent: Generating content for prompt: {prompt[:50]}...")
            
            # Generate content using Granite
            content = self.granite.generate(
                prompt=full_prompt,
                system_prompt=self.system_prompt,
                max_tokens=2048,
                temperature=0.7
            )
            
            logger.info(f"WriterAgent: Generated {len(content)} characters")
            
            # Log the API call to WatsonX logs via blog service
            try:
                async with httpx.AsyncClient(timeout=5.0) as log_client:
                    # Create a log entry by calling the blog service's internal logging
                    # We'll use the blog service's generate endpoint which logs automatically
                    pass  # Logging will be handled by using blog service API
            except Exception as log_error:
                logger.warning(f"WriterAgent: Failed to log API call: {str(log_error)}")
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

# Current Time
Current time in ISO 8601 UTC format: 2026-05-02T08:13:26.532Z
User time zone: America/New_York, UTC-4:00

# Current Cost
$0.52

# Review Exclusions
The following file patterns are excluded from code reviews:
- .vscode/**

# Current Mode
<slug>code</slug>
<name>💻 Code</name>
====

REMINDERS

Below is your current list of reminders for this task. Keep them updated as you progress.

| # | Content | Status |
|---|---------|--------|
| 1 | Fix writer agent manual run - blog not being saved to Home | Pending |
| 2 | Fix API calls not showing in API logs | Pending |
| 3 | Test the fixes | Pending |


IMPORTANT: When task status changes, remember to call the `update_todo_list` tool to update your progress.

</environment_details>

---

**Assistant:**

Actually, I need to take a better approach. Instead of trying to log separately, I should use the blog service's `/blogs/{blog_id}/generate` endpoint which already has logging built in. Let me rewrite the writer agent to use the blog service API properly:

<apply_diff>
<path>services/orchestration_service/agents/writer_agent.py</path>
<diff>
<<<<<<< SEARCH
:start_line:47
-------
    async def execute(self, input_data: Dict[str, Any]) -> AgentResult:
        """
        Generate blog content and save as draft
        
        Expected input_data:
        {
            "prompt": "Blog topic or instructions",
            "research_brief": "Optional research context",
            "tone": "Optional tone specification"
        }
        
        Returns:
            AgentResult with generated content and blog draft info
        """
        start_time = datetime.utcnow()
        
        try:
            prompt = input_data.get("prompt", "")
            research_brief = input_data.get("research_brief", "")
            tone = input_data.get("tone", "professional")
            
            if not prompt:
                return AgentResult(
                    success=False,
                    error="No prompt provided"
                )
            
            # Construct full prompt
            full_prompt = f"Topic: {prompt}\n\n"
            
            if research_brief:
                full_prompt += f"Research Context:\n{research_brief}\n\n"
            
            full_prompt += f"Tone: {tone}\n\n"
            full_prompt += "Write a complete blog post with title, introduction, body, and conclusion."
            
            logger.info(f"WriterAgent: Generating content for prompt: {prompt[:50]}...")
            
            # Generate content using Granite
            content = self.granite.generate(
                prompt=full_prompt,
                system_prompt=self.system_prompt,
                max_tokens=2048,
                temperature=0.7
            )
            
            logger.info(f"WriterAgent: Generated {len(content)} characters")
            
            # Log the API call to WatsonX logs via blog service
            try:
                async with httpx.AsyncClient(timeout=5.0) as log_client:
                    # Create a log entry by calling the blog service's internal logging
                    # We'll use the blog service's generate endpoint which logs automatically
                    pass  # Logging will be handled by using blog service API
            except Exception as log_error:
                logger.warning(f"WriterAgent: Failed to log API call: {str(log_error)}")
            
            # Extract title from content (first line or first heading)
            title = "Untitled Blog"
            content_lines = content.strip().split('\n')
            for line in content_lines:
                line = line.strip()
                if line:
                    # Remove markdown heading markers
                    title = line.lstrip('#').strip()
                    break
            
            # Create draft blog via blog service
            blog_id = None
            blog_created = False
            
            try:
                async with httpx.AsyncClient(timeout=30.0) as client:
                    # Create blog draft
                    blog_data = {
                        "title": title,
                        "description": f"Generated from prompt: {prompt[:100]}",
                        "tags": ["ai-generated", "draft"],
                        "publication_site": "Blog Platform",
                        "initial_prompt": prompt
                    }
                    
                    logger.info(f"WriterAgent: Creating draft blog via API...")
                    create_response = await client.post(
                        f"{BLOG_SERVICE_URL}/blogs",
                        json=blog_data
                    )
                    
                    if create_response.status_code == 200:
                        create_result = create_response.json()
                        if create_result.get("success"):
                            blog_id = create_result["data"]["id"]
                            blog_created = True
                            logger.info(f"WriterAgent: Created draft blog {blog_id}")
                            
                            # Update blog content
                            content_data = {"content": content}
                            update_response = await client.put(
                                f"{BLOG_SERVICE_URL}/blogs/{blog_id}/content",
                                json=content_data
                            )
                            
                            if update_response.status_code == 200:
                                logger.info(f"WriterAgent: Updated blog {blog_id} with generated content")
                            else:
                                logger.warning(f"WriterAgent: Failed to update blog content: {update_response.status_code}")
                    else:
                        logger.warning(f"WriterAgent: Failed to create blog: {create_response.status_code}")
                        
            except Exception as api_error:
                logger.error(f"WriterAgent: API call failed: {str(api_error)}")
                # Continue even if API call fails
            
            # Calculate processing time
            end_time = datetime.utcnow()
            processing_time_ms = int((end_time - start_time).total_seconds() * 1000)
            
            result_data = {
                "content": content,
                "word_count": len(content.split()),
                "char_count": len(content),
                "model": "ibm/granite-3-8b-instruct",
                "processing_time_ms": processing_time_ms
            }
            
            if blog_created and blog_id:
                result_data["blog_id"] = blog_id
                result_data["blog_status"] = "draft"
                result_data["blog_title"] = title
            
            return AgentResult(
                success=True,
                data=result_data,
                metadata={
                    "prompt": prompt,
                    "tone": tone,
                    "blog_created": blog_created
                }
            )
            
        except Exception as e:
            logger.error(f"WriterAgent: Failed to generate content: {str(e)}")
            return AgentResult(
                success=False,
                error=str(e)
            )
=======
    async def execute(self, input_data: Dict[str, Any]) -> AgentResult:
        """
        Generate blog content and save as draft
        
        Expected input_data:
        {
            "prompt": "Blog topic or instructions",
            "research_brief": "Optional research context",
            "tone": "Optional tone specification"
        }
        
        Returns:
            AgentResult with generated content and blog draft info
        """
        start_time = datetime.utcnow()
        
        try:
            prompt = input_data.get("prompt", "")
            research_brief = input_data.get("research_brief", "")
            tone = input_data.get("tone", "professional")
            
            if not prompt:
                return AgentResult(
                    success=False,
                    error="No prompt provided"
                )
            
            logger.info(f"WriterAgent: Generating content for prompt: {prompt[:50]}...")
            
            # Extract title from prompt for blog creation
            title_parts = prompt.split('\n')[0].strip()
            title = title_parts[:100] if title_parts else "AI Generated Blog"
            
            # Create draft blog via blog service FIRST
            blog_id = None
            blog_created = False
            
            try:
                async with httpx.AsyncClient(timeout=60.0) as client:
                    # Create blog draft
                    blog_data = {
                        "title": title,
                        "description": f"Generated from prompt: {prompt[:100]}",
                        "tags": ["ai-generated", "draft"],
                        "publication_site": "Blog Platform",
                        "initial_prompt": prompt
                    }
                    
                    logger.info(f"WriterAgent: Creating draft blog via API...")
                    create_response = await client.post(
                        f"{BLOG_SERVICE_URL}/blogs",
                        json=blog_data
                    )
                    
                    if create_response.status_code == 200:
                        create_result = create_response.json()
                        if create_result.get("success"):
                            blog_id = create_result["data"]["id"]
                            blog_created = True
                            logger.info(f"WriterAgent: Created draft blog {blog_id}")
                            
                            # Now generate content using blog service's generate endpoint
                            # This will properly log the API call to WatsonX logs
                            generate_data = {
                                "prompt": prompt,
                                "generation_type": "text"
                            }
                            
                            logger.info(f"WriterAgent: Generating content via blog service API...")
                            generate_response = await client.post(
                                f"{BLOG_SERVICE_URL}/blogs/{blog_id}/generate",
                                json=generate_data
                            )
                            
                            if generate_response.status_code == 200:
                                generate_result = generate_response.json()
                                if generate_result.get("success"):
                                    content = generate_result["data"]["content"]
                                    version = generate_result["data"]["version"]
                                    logger.info(f"WriterAgent: Generated content (version {version}) for blog {blog_id}")
                                    
                                    # Calculate processing time
                                    end_time = datetime.utcnow()
                                    processing_time_ms = int((end_time - start_time).total_seconds() * 1000)
                                    
                                    result_data = {
                                        "content": content,
                                        "word_count": len(content.split()),
                                        "char_count": len(content),
                                        "model": "ibm/granite-3-8b-instruct",
                                        "processing_time_ms": processing_time_ms,
                                        "blog_id": blog_id,
                                        "blog_status": "draft",
                                        "blog_title": title,
                                        "version": version
                                    }
                                    
                                    return AgentResult(
                                        success=True,
                                        data=result_data,
                                        metadata={
                                            "prompt": prompt,
                                            "tone": tone,
                                            "blog_created": True
                                        }
                                    )
                                else:
                                    error_msg = generate_result.get("message", "Content generation failed")
                                    logger.error(f"WriterAgent: {error_msg}")
                                    return AgentResult(
                                        success=False,
                                        error=error_msg
                                    )
                            else:
                                error_msg = f"Blog service returned status {generate_response.status_code}"
                                logger.error(f"WriterAgent: {error_msg}")
                                return AgentResult(
                                    success=False,
                                    error=error_msg
                                )
                    else:
                        error_msg = f"Failed to create blog: {create_response.status_code}"
                        logger.error(f"WriterAgent: {error_msg}")
                        return AgentResult(
                            success=False,
                            error=error_msg
                        )
                        
            except Exception as api_error:
                logger.error(f"WriterAgent: API call failed: {str(api_error)}")
                return AgentResult(
                    success=False,
                    error=f"API call failed: {str(api_error)}"
                )
            
        except Exception as e:
            logger.error(f"WriterAgent: Failed to generate content: {str(e)}")
            return AgentResult(
                success=False,
                error=str(e)
            )
>>>>>>> REPLACE
</diff>
</apply_diff>

---

**User:**

[apply_diff for 'services/orchestration_service/agents/writer_agent.py'] Result:
<file_write_result>
<path>services/orchestration_service/agents/writer_agent.py</path>
<operation>modified</operation>
<problems>

New problems detected after saving the file:
services/orchestration_service/agents/writer_agent.py
- [basedpyright Error] 47 |     async def execute(self, input_data: Dict[str, Any]) -&gt; AgentResult: : Function with declared return type "AgentResult" must return value on all code paths
  "None" is not assignable to "AgentResult"</problems>
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

# Current Time
Current time in ISO 8601 UTC format: 2026-05-02T08:14:03.869Z
User time zone: America/New_York, UTC-4:00

# Current Cost
$0.65

# Review Exclusions
The following file patterns are excluded from code reviews:
- .vscode/**

# Current Mode
<slug>code</slug>
<name>💻 Code</name>
====

REMINDERS

Below is your current list of reminders for this task. Keep them updated as you progress.

| # | Content | Status |
|---|---------|--------|
| 1 | Fix writer agent manual run - blog not being saved to Home | Pending |
| 2 | Fix API calls not showing in API logs | Pending |
| 3 | Test the fixes | Pending |


IMPORTANT: When task status changes, remember to call the `update_todo_list` tool to update your progress.

</environment_details>

---

**Assistant:**

I need to fix the return path issue. Let me add a fallback return statement:

<apply_diff>
<path>services/orchestration_service/agents/writer_agent.py</path>
<diff>
<<<<<<< SEARCH
:start_line:140
-------
            except Exception as api_error:
                logger.error(f"WriterAgent: API call failed: {str(api_error)}")
                return AgentResult(
                    success=False,
                    error=f"API call failed: {str(api_error)}"
                )
            
        except Exception as e:
            logger.error(f"WriterAgent: Failed to generate content: {str(e)}")
            return AgentResult(
                success=False,
                error=str(e)
            )
=======
            except Exception as api_error:
                logger.error(f"WriterAgent: API call failed: {str(api_error)}")
                return AgentResult(
                    success=False,
                    error=f"API call failed: {str(api_error)}"
                )
        
        except Exception as e:
            logger.error(f"WriterAgent: Failed to generate content: {str(e)}")
            return AgentResult(
                success=False,
                error=str(e)
            )
        
        # Fallback return (should never reach here)
        return AgentResult(
            success=False,
            error="Unexpected execution path"
        )
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

# Current Time
Current time in ISO 8601 UTC format: 2026-05-02T08:14:17.757Z
User time zone: America/New_York, UTC-4:00

# Current Cost
$0.78

# Review Exclusions
The following file patterns are excluded from code reviews:
- .vscode/**

# Current Mode
<slug>code</slug>
<name>💻 Code</name>
====

REMINDERS

Below is your current list of reminders for this task. Keep them updated as you progress.

| # | Content | Status |
|---|---------|--------|
| 1 | Fix writer agent manual run - blog not being saved to Home | Pending |
| 2 | Fix API calls not showing in API logs | Pending |
| 3 | Test the fixes | Pending |


IMPORTANT: When task status changes, remember to call the `update_todo_list` tool to update your progress.

</environment_details>

---

**Assistant:**

Good! Now let me update the todo list and restart the services to test the fixes:

<update_todo_list>
<todos>
[x] Fix writer agent manual run - blog not being saved to Home
[x] Fix API calls not showing in API logs
[ ] Test the fixes
</todos>
</update_todo_list>

---

**User:**

[update_todo_list] Result:
Todo list updated successfully.
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

# Current Time
Current time in ISO 8601 UTC format: 2026-05-02T08:14:30.923Z
User time zone: America/New_York, UTC-4:00

# Current Cost
$0.92

# Review Exclusions
The following file patterns are excluded from code reviews:
- .vscode/**

# Current Mode
<slug>code</slug>
<name>💻 Code</name>
====

REMINDERS

Below is your current list of reminders for this task. Keep them updated as you progress.

| # | Content | Status |
|---|---------|--------|
| 1 | Fix writer agent manual run - blog not being saved to Home | Completed |
| 2 | Fix API calls not showing in API logs | Completed |
| 3 | Test the fixes | Pending |


IMPORTANT: When task status changes, remember to call the `update_todo_list` tool to update your progress.

</environment_details>

---

**Assistant:**

Now let me restart the services to apply the changes:

<execute_command>
<command>cd c:\workspace\ForgeByBob && python stop_all_services.py && timeout /t 3 /nobreak && python start_all_services.py</command>
</execute_command>

---

**User:**

[execute_command for 'cd c:\workspace\ForgeByBob && python stop_all_services.py && timeout /t 3 /nobreak && python start_all_services.py'] Result:
Command executed in terminal  within working directory 'c:/workspace/ForgeByBob'. Command execution was not successful, inspect the cause and adjust as needed.
Exit code: 1
Output:
At line:1 char:28
+ cd c:\workspace\ForgeByBob && python stop_all_services.py && timeout  ...
+                            ~~
The token '&&' is not a valid statement separator in this version.
At line:1 char:59
+ cd c:\workspace\ForgeByBob && python stop_all_services.py && timeout  ...
+                                                           ~~
The token '&&' is not a valid statement separator in this version.
At line:1 char:84
+ ... ob && python stop_all_services.py && timeout /t 3 /nobreak && python  ...
+                                                                ~~
The token '&&' is not a valid statement separator in this version.
    + CategoryInfo          : ParserError: (:) [], ParentContainsErrorRecordException
    + FullyQualifiedErrorId : InvalidEndOfLine
 

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

# Current Time
Current time in ISO 8601 UTC format: 2026-05-02T08:14:44.245Z
User time zone: America/New_York, UTC-4:00

# Current Cost
$1.06

# Review Exclusions
The following file patterns are excluded from code reviews:
- .vscode/**

# Current Mode
<slug>code</slug>
<name>💻 Code</name>
====

REMINDERS

Below is your current list of reminders for this task. Keep them updated as you progress.

| # | Content | Status |
|---|---------|--------|
| 1 | Fix writer agent manual run - blog not being saved to Home | Completed |
| 2 | Fix API calls not showing in API logs | Completed |
| 3 | Test the fixes | Pending |


IMPORTANT: When task status changes, remember to call the `update_todo_list` tool to update your progress.

</environment_details>

---

**Assistant:**

Let me use PowerShell syntax:

<execute_command>
<command>python stop_all_services.py; Start-Sleep -Seconds 3; python start_all_services.py</command>
</execute_command>

