**User:**

<task>
still getting error "{"detail":"Model 'ibm/granite-4-0-h-small' is not supported for this environment. Supported models: ['cross-encoder/ms-marco-minilm-l-12-v2', 'ibm/granite-3-1-8b-base', 'ibm/granite-4-h-small', 'ibm/granite-8b-code-instruct', 'ibm/granite-embedding-278m-multilingual', 'ibm/granite-guardian-3-8b', 'ibm/granite-ttm-1024-96-r2', 'ibm/granite-ttm-1536-96-r2', 'ibm/granite-ttm-512-96-r2', 'ibm/slate-125m-english-rtrvr-v2', 'ibm/slate-30m-english-rtrvr-v2', 'intfloat/multilingual-e5-large', 'meta-llama/llama-3-1-70b-gptq', 'meta-llama/llama-3-1-8b', 'meta-llama/llama-3-2-11b-vision-instruct', 'meta-llama/llama-3-3-70b-instruct', 'meta-llama/llama-4-maverick-17b-128e-instruct-fp8', 'meta-llama/llama-guard-3-11b-vision', 'mistral-large-2512', 'mistralai/mistral-medium-2505', 'mistralai/mistral-small-3-1-24b-instruct-2503', 'openai/gpt-oss-120b', 'sentence-transformers/all-minilm-l6-v2']"}"
</task>
<environment_details>
# VSCode Visible Files
.env

# VSCode Open Tabs
services/blog_service/main.py,.env

# Actively Running Terminals
## Terminal 1 (Active)
### Working Directory: `c:\workspace\ForgeByBob`
### Original command: `Stop-Process -Name python -Force -ErrorAction SilentlyContinue; Start-Sleep -Seconds 2; python start_all_services.py`
### New Output
INFO:     Waiting for application startup.
INFO:     Application startup complete.
ERROR:    [Errno 10048] error while attempting to bind on address ('0.0.0.0', 8003): [winerror 10048] only one usage of each socket address (protocol/network address/port) is normally permitted
INFO:     Waiting for application shutdown.
INFO:     Application shutdown complete.

## Terminal 2 (Active)
### Working Directory: `c:\workspace\ForgeByBob`
### Original command: `python start_all_services.py`

# Current Time
Current time in ISO 8601 UTC format: 2026-05-02T04:27:43.829Z
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

I'll help you fix this error. The issue is that you're trying to use the model `ibm/granite-4-0-h-small`, but the correct model name according to the error message is `ibm/granite-4-h-small` (without the `-0`).

Let me first check the current configuration to see where this model name is being used:

<read_file>
<args>
<file>
<path>.env</path>
</file>
<file>
<path>services/watsonx_service/config.py</path>
</file>
<file>
<path>services/watsonx_service/granite_client.py</path>
</file>
<file>
<path>services/watsonx_service/main.py</path>
</file>
</args>
</read_file>

---

**User:**

[read_file for 4 files] Result:
<files>
<file><path>.env</path>
<content lines="1-101">
  1 | # Environment Variables Template for IBM Bob Hackathon
  2 | # Copy this file to .env and fill in your actual values
  3 | # IMPORTANT: Never commit the .env file to version control!
  4 | 
  5 | # =============================================================================
  6 | # REQUIRED: IBM Cloud Authentication
  7 | # =============================================================================
  8 | # Get your API key from: IBM Cloud Dashboard → Profile → API keys
  9 | # See IBM_CREDENTIALS_SETUP_GUIDE.md for detailed instructions
 10 | IBM_CLOUD_API_KEY=your_ibm_cloud_api_key_here
 11 | 
 12 | # =============================================================================
 13 | # REQUIRED: IBM watsonx.ai Configuration
 14 | # =============================================================================
 15 | # Create project at: https://dataplatform.cloud.ibm.com/
 16 | # Copy PROJECT_ID from the project URL after creation
 17 | WATSONX_PROJECT_ID=your_watsonx_project_id_here
 18 | WATSONX_URL=https://us-south.ml.cloud.ibm.com
 19 | # Using Granite 4 H Small - optimized for efficiency and lower rate limits
 20 | WATSONX_MODEL_ID=ibm/granite-4-h-small
 21 | 
 22 | # =============================================================================
 23 | # REQUIRED: IBM Cloud Object Storage (COS)
 24 | # =============================================================================
 25 | # Use your hackathon-provisioned COS instance
 26 | COS_INSTANCE_ID=1acbd021-33e4-49aa-8d8a-308e67588a71
 27 | COS_API_KEY=${IBM_CLOUD_API_KEY}
 28 | COS_ENDPOINT=https://s3.us-south.cloud-object-storage.appdomain.cloud
 29 | COS_BUCKET=blogagent-storage
 30 | 
 31 | # =============================================================================
 32 | # IBM watsonx Orchestrate (for agent coordination)
 33 | # =============================================================================
 34 | ORCHESTRATE_INSTANCE_ID=watsonx-Hackathon_Orchestrate
 35 | ORCHESTRATE_API_KEY=${IBM_CLOUD_API_KEY}
 36 | ORCHESTRATE_URL=https://orchestrate.watsonx.ibm.com
 37 | ORCHESTRATE_WORKSPACE_ID=your_workspace_id_here
 38 | 
 39 | # =============================================================================
 40 | # IBM Watson Natural Language Understanding (for enhanced research)
 41 | # =============================================================================
 42 | NLU_INSTANCE_ID=watsonx-Hackathon_NLU
 43 | NLU_API_KEY=${IBM_CLOUD_API_KEY}
 44 | NLU_URL=https://api.us-south.natural-language-understanding.watson.cloud.ibm.com
 45 | 
 46 | # =============================================================================
 47 | # IBM Cloudant Database (for pipeline history and analytics)
 48 | # =============================================================================
 49 | CLOUDANT_INSTANCE_ID=watsonx-Hackathon_Cloudant
 50 | CLOUDANT_API_KEY=${IBM_CLOUD_API_KEY}
 51 | CLOUDANT_URL=https://01b7e99f-48a0-4d2c-873f-b60daf388b62-bluemix.cloudant.com/
 52 | CLOUDANT_ACCOUNT=your_cloudant_account_here
 53 | CLOUDANT_DATABASE=pipeline_history
 54 | 
 55 | # =============================================================================
 56 | # IBM watsonx Governance (for compliance and audit trails)
 57 | # =============================================================================
 58 | GOV_INSTANCE_ID=watsonx-Hackathon_GOV
 59 | GOV_API_KEY=${IBM_CLOUD_API_KEY}
 60 | GOV_URL=https://api.dataplatform.cloud.ibm.com/v2/governance
 61 | 
 62 | # =============================================================================
 63 | # OPTIONAL: Legacy Gemini AI (for fallback during migration)
 64 | # =============================================================================
 65 | # GEMINI_API_KEY=your_gemini_api_key_here
 66 | # USE_GRANITE=true
 67 | # FALLBACK_TO_GEMINI=false
 68 | 
 69 | # =============================================================================
 70 | # REQUIRED: Security Configuration
 71 | # =============================================================================
 72 | # Generate a secure secret key using: python -c "import secrets; print(secrets.token_urlsafe(32))"
 73 | SECRET_KEY=your_secret_key_here_CHANGE_THIS_IN_PRODUCTION
 74 | 
 75 | # =============================================================================
 76 | # Application Settings
 77 | # =============================================================================
 78 | SOURCE_FOLDER=./blogs
 79 | DATABASE_URL=sqlite:///./app.db
 80 | ACCESS_TOKEN_EXPIRE_MINUTES=30
 81 | LOG_LEVEL=INFO
 82 | 
 83 | # Agent Configuration
 84 | MAX_ITERATIONS=3
 85 | QUALITY_THRESHOLD=7.0
 86 | 
 87 | # =============================================================================
 88 | # Service Ports (change if ports are already in use)
 89 | # =============================================================================
 90 | API_GATEWAY_PORT=8000
 91 | BLOG_SERVICE_PORT=8001
 92 | SETTINGS_SERVICE_PORT=8002
 93 | UI_SERVICE_PORT=8003
 94 | ORCHESTRATION_SERVICE_PORT=8004
 95 | 
 96 | # =============================================================================
 97 | # Service URLs (for inter-service communication)
 98 | # =============================================================================
 99 | BLOG_SERVICE_URL=http://localhost:8001
100 | SETTINGS_SERVICE_URL=http://localhost:8002
101 | ORCHESTRATION_SERVICE_URL=http://localhost:8004
</content>
</file>
<file><path>services/watsonx_service/config.py</path>
<content lines="1-49">
 1 | """
 2 | Configuration for IBM watsonx.ai Granite client
 3 | """
 4 | from pydantic import BaseModel
 5 | from typing import Optional
 6 | import os
 7 | from dotenv import load_dotenv
 8 | 
 9 | # Load environment variables from .env file
10 | load_dotenv()
11 | 
12 | 
13 | class GraniteConfig(BaseModel):
14 |     """Configuration for Granite LLM"""
15 |     
16 |     # IBM Cloud credentials
17 |     api_key: str
18 |     project_id: str
19 |     url: str = "https://us-south.ml.cloud.ibm.com"
20 |     
21 |     # Model configuration
22 |     model_id: str = "ibm/granite-4-h-small"
23 |     
24 |     # Generation parameters
25 |     max_new_tokens: int = 2048
26 |     temperature: float = 0.7
27 |     top_p: float = 0.9
28 |     top_k: int = 50
29 |     repetition_penalty: float = 1.1
30 |     
31 |     @classmethod
32 |     def from_env(cls) -> "GraniteConfig":
33 |         """Load configuration from environment variables"""
34 |         return cls(
35 |             api_key=os.getenv("IBM_CLOUD_API_KEY", ""),
36 |             project_id=os.getenv("WATSONX_PROJECT_ID", ""),
37 |             url=os.getenv("WATSONX_URL", "https://us-south.ml.cloud.ibm.com"),
38 |             model_id=os.getenv("WATSONX_MODEL_ID", "ibm/granite-3-8b-instruct")
39 |         )
40 |     
41 |     def validate_credentials(self) -> bool:
42 |         """Validate that required credentials are present"""
43 |         return bool(self.api_key and self.project_id)
44 | 
45 | 
46 | # Global config instance
47 | granite_config = GraniteConfig.from_env()
48 | 
49 | # Made with Bob
</content>
</file>
<file><path>services/watsonx_service/granite_client.py</path>
<content lines="1-223">
  1 | """
  2 | IBM watsonx.ai Granite LLM Client
  3 | """
  4 | from ibm_watsonx_ai.foundation_models import ModelInference
  5 | from ibm_watsonx_ai.metanames import GenTextParamsMetaNames as GenParams
  6 | from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
  7 | from typing import Optional, Dict, Any
  8 | import logging
  9 | import json
 10 | 
 11 | from .config import granite_config
 12 | 
 13 | logger = logging.getLogger(__name__)
 14 | 
 15 | 
 16 | class GraniteClient:
 17 |     """Client for IBM watsonx.ai foundation models"""
 18 |     
 19 |     def __init__(self, config: Optional[Any] = None):
 20 |         """
 21 |         Initialize watsonx client
 22 |         
 23 |         Args:
 24 |             config: Optional GraniteConfig instance. If None, uses global config.
 25 |         """
 26 |         self.config = config or granite_config
 27 |         
 28 |         if not self.config.validate_credentials():
 29 |             raise ValueError(
 30 |                 "IBM watsonx credentials not configured. "
 31 |                 "Set IBM_CLOUD_API_KEY and WATSONX_PROJECT_ID in .env"
 32 |             )
 33 |         
 34 |         # Initialize IBM watsonx.ai model
 35 |         self.model = self._initialize_model()
 36 |         logger.info(f"watsonx client initialized with model: {self.config.model_id}")
 37 |     
 38 |     def _initialize_model(self) -> ModelInference:
 39 |         """Initialize the watsonx model"""
 40 |         try:
 41 |             # Disable retries to fail fast on rate limits
 42 |             model = ModelInference(
 43 |                 model_id=self.config.model_id,
 44 |                 params={
 45 |                     GenParams.MAX_NEW_TOKENS: self.config.max_new_tokens,
 46 |                     GenParams.TEMPERATURE: self.config.temperature,
 47 |                     GenParams.TOP_P: self.config.top_p,
 48 |                     GenParams.TOP_K: self.config.top_k,
 49 |                     GenParams.REPETITION_PENALTY: self.config.repetition_penalty,
 50 |                 },
 51 |                 credentials={
 52 |                     "apikey": self.config.api_key,
 53 |                     "url": self.config.url
 54 |                 },
 55 |                 project_id=self.config.project_id,
 56 |                 verify=False  # Disable SSL verification if needed
 57 |             )
 58 |             return model
 59 |         except Exception as e:
 60 |             logger.error(f"Failed to initialize watsonx model: {str(e)}")
 61 |             raise
 62 |     
 63 |     def generate(
 64 |         self,
 65 |         prompt: str,
 66 |         system_prompt: Optional[str] = None,
 67 |         max_tokens: Optional[int] = None,
 68 |         temperature: Optional[float] = None
 69 |     ) -> str:
 70 |         """
 71 |         Generate text using watsonx model
 72 |         
 73 |         Args:
 74 |             prompt: User prompt
 75 |             system_prompt: Optional system prompt for context
 76 |             max_tokens: Override default max_new_tokens
 77 |             temperature: Override default temperature
 78 |             
 79 |         Returns:
 80 |             Generated text
 81 |         """
 82 |         try:
 83 |             # Construct full prompt with system context
 84 |             full_prompt = self._construct_prompt(prompt, system_prompt)
 85 |             
 86 |             # Override parameters if provided
 87 |             params = {}
 88 |             if max_tokens:
 89 |                 params[GenParams.MAX_NEW_TOKENS] = max_tokens
 90 |             if temperature is not None:
 91 |                 params[GenParams.TEMPERATURE] = temperature
 92 |             
 93 |             # Generate text
 94 |             logger.info(f"Generating with watsonx (prompt length: {len(full_prompt)} chars)")
 95 |             
 96 |             if params:
 97 |                 # Create temporary model with custom params
 98 |                 temp_model = ModelInference(
 99 |                     model_id=self.config.model_id,
100 |                     params={
101 |                         GenParams.MAX_NEW_TOKENS: params.get(GenParams.MAX_NEW_TOKENS, self.config.max_new_tokens),
102 |                         GenParams.TEMPERATURE: params.get(GenParams.TEMPERATURE, self.config.temperature),
103 |                         GenParams.TOP_P: self.config.top_p,
104 |                         GenParams.TOP_K: self.config.top_k,
105 |                         GenParams.REPETITION_PENALTY: self.config.repetition_penalty,
106 |                     },
107 |                     credentials={"apikey": self.config.api_key, "url": self.config.url},
108 |                     project_id=self.config.project_id
109 |                 )
110 |                 response = temp_model.generate_text(prompt=full_prompt)
111 |             else:
112 |                 response = self.model.generate_text(prompt=full_prompt)
113 |             
114 |             # Ensure response is a string
115 |             if isinstance(response, dict):
116 |                 response = response.get('results', [{}])[0].get('generated_text', '')
117 |             elif isinstance(response, list):
118 |                 response = response[0] if response else ''
119 |             
120 |             logger.info(f"watsonx generation successful (response length: {len(response)} chars)")
121 |             return str(response)
122 |             
123 |         except Exception as e:
124 |             error_msg = str(e)
125 |             # Check for rate limit error
126 |             if "429" in error_msg or "Too Many Requests" in error_msg:
127 |                 logger.error("Rate limit exceeded. Please wait 5 minutes before trying again.")
128 |                 raise ValueError(
129 |                     "IBM watsonx.ai rate limit exceeded. "
130 |                     "Please wait 5 minutes before generating more content. "
131 |                     "This is normal with the free tier plan."
132 |                 )
133 |             logger.error(f"watsonx generation failed: {error_msg}")
134 |             raise
135 |     
136 |     def generate_structured(
137 |         self,
138 |         prompt: str,
139 |         schema: Dict[str, Any],
140 |         system_prompt: Optional[str] = None
141 |     ) -> Dict[str, Any]:
142 |         """
143 |         Generate structured JSON output
144 |         
145 |         Args:
146 |             prompt: User prompt
147 |             schema: JSON schema for expected output
148 |             system_prompt: Optional system prompt
149 |             
150 |         Returns:
151 |             Parsed JSON object
152 |         """
153 |         response = ""
154 |         try:
155 |             # Add JSON schema instruction to prompt
156 |             json_instruction = (
157 |                 f"\n\nRespond with valid JSON matching this schema:\n"
158 |                 f"```json\n{json.dumps(schema, indent=2)}\n```\n"
159 |                 f"Return ONLY the JSON object, no additional text."
160 |             )
161 |             
162 |             full_prompt = prompt + json_instruction
163 |             
164 |             # Generate response
165 |             response = self.generate(full_prompt, system_prompt)
166 |             
167 |             # Extract JSON from response (handle markdown code blocks)
168 |             json_text = self._extract_json(response)
169 |             
170 |             # Parse JSON
171 |             result = json.loads(json_text)
172 |             logger.info("Structured generation successful")
173 |             return result
174 |             
175 |         except json.JSONDecodeError as e:
176 |             logger.error(f"Failed to parse JSON response: {str(e)}")
177 |             logger.error(f"Response was: {response}")
178 |             raise ValueError(f"Invalid JSON response from watsonx: {str(e)}")
179 |         except Exception as e:
180 |             logger.error(f"Structured generation failed: {str(e)}")
181 |             raise
182 |     
183 |     def _construct_prompt(self, prompt: str, system_prompt: Optional[str] = None) -> str:
184 |         """Construct full prompt with system context"""
185 |         if system_prompt:
186 |             return f"{system_prompt}\n\n{prompt}"
187 |         return prompt
188 |     
189 |     def _extract_json(self, text: str) -> str:
190 |         """Extract JSON from text (handles markdown code blocks)"""
191 |         # Remove markdown code blocks if present
192 |         if "```json" in text:
193 |             start = text.find("```json") + 7
194 |             end = text.find("```", start)
195 |             return text[start:end].strip()
196 |         elif "```" in text:
197 |             start = text.find("```") + 3
198 |             end = text.find("```", start)
199 |             return text[start:end].strip()
200 |         return text.strip()
201 |     
202 |     def test_connection(self) -> bool:
203 |         """Test connection to IBM watsonx.ai"""
204 |         try:
205 |             response = self.generate("Say 'Hello from Granite!'", max_tokens=50)
206 |             return "Granite" in response or "Hello" in response
207 |         except Exception as e:
208 |             logger.error(f"Connection test failed: {str(e)}")
209 |             return False
210 | 
211 | 
212 | # Global client instance
213 | _granite_client: Optional[GraniteClient] = None
214 | 
215 | 
216 | def get_granite_client() -> GraniteClient:
217 |     """Get or create global Granite client instance"""
218 |     global _granite_client
219 |     if _granite_client is None:
220 |         _granite_client = GraniteClient()
221 |     return _granite_client
222 | 
223 | # Made with Bob
</content>
</file>
<file><path>services/watsonx_service/main.py</path>
<content lines="1-211">
  1 | """
  2 | IBM watsonx.ai Service - FastAPI microservice for Granite LLM
  3 | """
  4 | from fastapi import FastAPI, HTTPException
  5 | from pydantic import BaseModel
  6 | from typing import Optional, Dict, Any
  7 | import logging
  8 | 
  9 | from .granite_client import get_granite_client, GraniteClient
 10 | from .config import granite_config
 11 | 
 12 | # Configure logging
 13 | logging.basicConfig(level=logging.INFO)
 14 | logger = logging.getLogger(__name__)
 15 | 
 16 | app = FastAPI(
 17 |     title="IBM watsonx.ai Service",
 18 |     description="Microservice for IBM Granite LLM text generation",
 19 |     version="1.0.0"
 20 | )
 21 | 
 22 | # Global client instance
 23 | granite_client: Optional[GraniteClient] = None
 24 | 
 25 | 
 26 | class GenerateRequest(BaseModel):
 27 |     """Request model for text generation"""
 28 |     prompt: str
 29 |     system_prompt: Optional[str] = None
 30 |     max_tokens: Optional[int] = None
 31 |     temperature: Optional[float] = None
 32 | 
 33 | 
 34 | class GenerateResponse(BaseModel):
 35 |     """Response model for text generation"""
 36 |     success: bool
 37 |     text: str
 38 |     model: str
 39 |     tokens_used: Optional[int] = None
 40 | 
 41 | 
 42 | class StructuredGenerateRequest(BaseModel):
 43 |     """Request model for structured JSON generation"""
 44 |     prompt: str
 45 |     json_schema: Dict[str, Any]
 46 |     system_prompt: Optional[str] = None
 47 | 
 48 | 
 49 | class StructuredGenerateResponse(BaseModel):
 50 |     """Response model for structured generation"""
 51 |     success: bool
 52 |     data: Dict[str, Any]
 53 |     model: str
 54 | 
 55 | 
 56 | class HealthResponse(BaseModel):
 57 |     """Health check response"""
 58 |     status: str
 59 |     service: str
 60 |     model: str
 61 |     credentials_valid: bool
 62 | 
 63 | 
 64 | @app.on_event("startup")
 65 | async def startup_event():
 66 |     """Initialize Granite client on startup"""
 67 |     global granite_client
 68 |     try:
 69 |         granite_client = get_granite_client()
 70 |         logger.info("IBM watsonx.ai service started successfully")
 71 |     except Exception as e:
 72 |         logger.error(f"Failed to initialize Granite client: {str(e)}")
 73 |         # Don't fail startup, allow health check to report the issue
 74 | 
 75 | 
 76 | @app.get("/", response_model=HealthResponse)
 77 | async def root():
 78 |     """Root endpoint with service information"""
 79 |     return HealthResponse(
 80 |         status="running",
 81 |         service="IBM watsonx.ai Service",
 82 |         model=granite_config.model_id,
 83 |         credentials_valid=granite_config.validate_credentials()
 84 |     )
 85 | 
 86 | 
 87 | @app.get("/health", response_model=HealthResponse)
 88 | async def health_check():
 89 |     """Health check endpoint"""
 90 |     try:
 91 |         if granite_client is None:
 92 |             return HealthResponse(
 93 |                 status="error",
 94 |                 service="IBM watsonx.ai Service",
 95 |                 model=granite_config.model_id,
 96 |                 credentials_valid=False
 97 |             )
 98 |         
 99 |         # Test connection
100 |         connection_ok = granite_client.test_connection()
101 |         
102 |         return HealthResponse(
103 |             status="healthy" if connection_ok else "unhealthy",
104 |             service="IBM watsonx.ai Service",
105 |             model=granite_config.model_id,
106 |             credentials_valid=granite_config.validate_credentials()
107 |         )
108 |     except Exception as e:
109 |         logger.error(f"Health check failed: {str(e)}")
110 |         return HealthResponse(
111 |             status="error",
112 |             service="IBM watsonx.ai Service",
113 |             model=granite_config.model_id,
114 |             credentials_valid=False
115 |         )
116 | 
117 | 
118 | @app.post("/generate", response_model=GenerateResponse)
119 | async def generate_text(request: GenerateRequest):
120 |     """
121 |     Generate text using IBM Granite model
122 |     
123 |     Args:
124 |         request: Generation request with prompt and optional parameters
125 |         
126 |     Returns:
127 |         Generated text response
128 |     """
129 |     try:
130 |         if granite_client is None:
131 |             raise HTTPException(
132 |                 status_code=503,
133 |                 detail="IBM watsonx client not initialized. Check credentials."
134 |             )
135 |         
136 |         # Generate text
137 |         text = granite_client.generate(
138 |             prompt=request.prompt,
139 |             system_prompt=request.system_prompt,
140 |             max_tokens=request.max_tokens,
141 |             temperature=request.temperature
142 |         )
143 |         
144 |         return GenerateResponse(
145 |             success=True,
146 |             text=text,
147 |             model=granite_config.model_id,
148 |             tokens_used=None  # IBM SDK doesn't provide token count in response
149 |         )
150 |         
151 |     except Exception as e:
152 |         logger.error(f"Text generation failed: {str(e)}")
153 |         raise HTTPException(status_code=500, detail=str(e))
154 | 
155 | 
156 | @app.post("/generate/structured", response_model=StructuredGenerateResponse)
157 | async def generate_structured(request: StructuredGenerateRequest):
158 |     """
159 |     Generate structured JSON output using IBM Granite model
160 |     
161 |     Args:
162 |         request: Structured generation request with prompt and schema
163 |         
164 |     Returns:
165 |         Parsed JSON object matching the schema
166 |     """
167 |     try:
168 |         if granite_client is None:
169 |             raise HTTPException(
170 |                 status_code=503,
171 |                 detail="IBM watsonx client not initialized. Check credentials."
172 |             )
173 |         
174 |         # Generate structured output
175 |         data = granite_client.generate_structured(
176 |             prompt=request.prompt,
177 |             schema=request.json_schema,
178 |             system_prompt=request.system_prompt
179 |         )
180 |         
181 |         return StructuredGenerateResponse(
182 |             success=True,
183 |             data=data,
184 |             model=granite_config.model_id
185 |         )
186 |         
187 |     except Exception as e:
188 |         logger.error(f"Structured generation failed: {str(e)}")
189 |         raise HTTPException(status_code=500, detail=str(e))
190 | 
191 | 
192 | @app.get("/config")
193 | async def get_config():
194 |     """Get current configuration (without sensitive data)"""
195 |     return {
196 |         "model_id": granite_config.model_id,
197 |         "url": granite_config.url,
198 |         "max_new_tokens": granite_config.max_new_tokens,
199 |         "temperature": granite_config.temperature,
200 |         "top_p": granite_config.top_p,
201 |         "top_k": granite_config.top_k,
202 |         "repetition_penalty": granite_config.repetition_penalty,
203 |         "credentials_configured": granite_config.validate_credentials()
204 |     }
205 | 
206 | 
207 | if __name__ == "__main__":
208 |     import uvicorn
209 |     uvicorn.run(app, host="0.0.0.0", port=8005)
210 | 
211 | # Made with Bob
</content>
</file>
</files>
<environment_details>
# VSCode Visible Files
.env

# VSCode Open Tabs
services/blog_service/main.py,.env

# Actively Running Terminals
## Terminal 1 (Active)
### Working Directory: `c:\workspace\ForgeByBob`
### Original command: `Stop-Process -Name python -Force -ErrorAction SilentlyContinue; Start-Sleep -Seconds 2; python start_all_services.py`
## Terminal 2 (Active)
### Working Directory: `c:\workspace\ForgeByBob`
### Original command: `python start_all_services.py`

# Current Time
Current time in ISO 8601 UTC format: 2026-05-02T04:27:48.880Z
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

I can see the issue! The `.env` file has the correct model name `ibm/granite-4-h-small` on line 20, but the `config.py` file has a fallback default value on line 38 that uses the old incorrect model name `ibm/granite-3-8b-instruct`. 

However, looking at the error message more carefully, it seems the model name being used is `ibm/granite-4-0-h-small` (with `-0-`), which doesn't match either. Let me search for where this incorrect model name might be coming from:

<search_files>
<path>.</path>
<regex>granite-4-0-h-small</regex>
<file_pattern>*.py</file_pattern>
</search_files>

---

**User:**

[search_files for 'granite-4-0-h-small' in '*.py'] Result:
Found 0 results.
<environment_details>
# VSCode Visible Files
.env

# VSCode Open Tabs
services/blog_service/main.py,.env

# Actively Running Terminals
## Terminal 1 (Active)
### Working Directory: `c:\workspace\ForgeByBob`
### Original command: `Stop-Process -Name python -Force -ErrorAction SilentlyContinue; Start-Sleep -Seconds 2; python start_all_services.py`
## Terminal 2 (Active)
### Working Directory: `c:\workspace\ForgeByBob`
### Original command: `python start_all_services.py`

# Current Time
Current time in ISO 8601 UTC format: 2026-05-02T04:27:55.382Z
User time zone: America/New_York, UTC-4:00

# Current Cost
$0.04

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

Let me check if there's a cached environment or if the services need to be restarted to pick up the correct model name. First, let me verify the actual .env file content and also check the blog service which might be making the watsonx calls:

<read_file>
<args>
<file>
<path>services/blog_service/main.py</path>
</file>
</args>
</read_file>

---

**User:**

[read_file for 'services/blog_service/main.py'. Reading multiple files at once is more efficient for the LLM. If other files are relevant to your current task, please read them simultaneously.] Result:
<files>
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
.env

# VSCode Open Tabs
services/blog_service/main.py,.env

# Actively Running Terminals
## Terminal 1 (Active)
### Working Directory: `c:\workspace\ForgeByBob`
### Original command: `Stop-Process -Name python -Force -ErrorAction SilentlyContinue; Start-Sleep -Seconds 2; python start_all_services.py`
## Terminal 2 (Active)
### Working Directory: `c:\workspace\ForgeByBob`
### Original command: `python start_all_services.py`

# Current Time
Current time in ISO 8601 UTC format: 2026-05-02T04:27:59.739Z
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

I found the issue! Looking at line 311 in `services/blog_service/main.py`, there's a hardcoded model name in the `log_watsonx_request` function that uses `"ibm/granite-4-h-small"` as the default. However, the error message shows `ibm/granite-4-0-h-small` is being used somewhere.

The problem is that the `.env` file has the correct model name, but the services might be using cached environment variables or there might be another configuration file. Let me restart the services to pick up the correct environment variables:

<execute_command>
<command>Stop-Process -Name python -Force -ErrorAction SilentlyContinue; Start-Sleep -Seconds 2; python start_all_services.py</command>
</execute_command>

