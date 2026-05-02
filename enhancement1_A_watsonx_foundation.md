# Enhancement 1-A: IBM watsonx Foundation Setup

## Module Overview
This is the foundational module that sets up IBM watsonx.ai and replaces Google Gemini with IBM Granite models. This module is **fully functional** on its own and provides immediate value by migrating to IBM's LLM platform.

## What This Module Delivers
- ✅ IBM Cloud account and watsonx.ai instance configured
- ✅ Granite 3.3 8B Instruct model deployed and accessible
- ✅ Complete replacement of Gemini API calls with Granite
- ✅ Functional blog generation using IBM Granite
- ✅ Cost tracking and monitoring setup

## Prerequisites
- IBM Cloud account (free tier available)
- Python 3.11+
- Existing ForgeByBob application running

## Implementation Time: 2-3 hours

---

## Part 1: IBM Cloud & watsonx.ai Setup (45 minutes)

### Step 1.1: Create IBM Cloud Account

**Action Steps:**
1. Navigate to https://cloud.ibm.com/registration
2. Fill in registration form:
   - Email address
   - Password (min 8 characters, uppercase, lowercase, number)
   - Country/Region
3. Verify email address (check inbox for verification link)
4. Complete profile setup
5. Choose "Lite" (free) plan when prompted

**Expected Result:**
- IBM Cloud dashboard accessible at https://cloud.ibm.com/
- Account status: Active
- Free tier credits available

### Step 1.2: Create watsonx.ai Instance

**Action Steps:**
1. Log into IBM Cloud dashboard
2. Click "Catalog" in top navigation
3. Search for "watsonx.ai"
4. Click on "watsonx.ai" service
5. Configure instance:
   ```
   Service name: watsonx-blogagent
   Region: Dallas (us-south) [recommended for best performance]
   Pricing plan: Lite (Free)
   Resource group: Default
   ```
6. Click "Create"
7. Wait 2-3 minutes for provisioning

**Expected Result:**
- watsonx.ai instance appears in "Resource list"
- Status: Active
- Instance URL available

**Screenshot Checkpoints:**
- ✓ watsonx.ai instance in resource list
- ✓ "Active" status indicator
- ✓ "Launch watsonx.ai" button visible

### Step 1.3: Access watsonx.ai Platform

**Action Steps:**
1. From IBM Cloud dashboard, go to "Resource list"
2. Under "AI / Machine Learning", click "watsonx-blogagent"
3. Click "Launch watsonx.ai" button
4. You'll be redirected to watsonx.ai platform (https://dataplatform.cloud.ibm.com/)

**Expected Result:**
- watsonx.ai platform interface loads
- Left sidebar shows: Projects, Deployments, Prompt Lab, etc.

### Step 1.4: Create watsonx.ai Project

**Action Steps:**
1. In watsonx.ai platform, click "Projects" in left sidebar
2. Click "New project" button
3. Select "Create an empty project"
4. Fill in project details:
   ```
   Name: BlogAgent Pro
   Description: AI-powered blog generation with autonomous agents
   Storage: Create new Cloud Object Storage (automatic)
   ```
5. Click "Create"

**Expected Result:**
- Project "BlogAgent Pro" created
- Project ID visible in URL: `https://dataplatform.cloud.ibm.com/projects/{PROJECT_ID}`
- Copy and save this PROJECT_ID - you'll need it later

**Important:** Save your PROJECT_ID immediately:
```bash
# Example PROJECT_ID format
PROJECT_ID=12345678-abcd-1234-efgh-123456789012
```

### Step 1.5: Generate API Key

**Action Steps:**
1. Click on your profile icon (top right)
2. Select "Profile and settings"
3. Click "API keys" tab
4. Click "Create +" button
5. Fill in API key details:
   ```
   Name: watsonx-blogagent-key
   Description: API key for BlogAgent Pro application
   ```
6. Click "Create"
7. **CRITICAL:** Copy the API key immediately (shown only once)
8. Store securely - you cannot retrieve it again

**Expected Result:**
- API key generated (format: `xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx`)
- API key saved securely

**Security Note:**
```bash
# NEVER commit this to git
# Store in .env file only
IBM_CLOUD_API_KEY=your_api_key_here
```

### Step 1.6: Access Granite Models

**Action Steps:**
1. In watsonx.ai platform, click "Prompt Lab" in left sidebar
2. Click "View all foundation models"
3. Find "Granite 3.3 8B Instruct" in the list
4. Click on it to view details
5. Note the model ID: `ibm/granite-3-8b-instruct`
6. Click "Try in Prompt Lab" to test

**Test the Model:**
```
Prompt: Write a short blog introduction about artificial intelligence.

Expected Output: A coherent 2-3 paragraph introduction about AI
```

**Expected Result:**
- Granite model responds with quality text
- Response time: 2-5 seconds
- Model ID confirmed: `ibm/granite-3-8b-instruct`

---

## Part 2: Environment Configuration (15 minutes)

### Step 2.1: Update .env File

**Action Steps:**
1. Open your `.env` file in the project root
2. Add IBM watsonx configuration:

```bash
# IBM watsonx.ai Configuration
IBM_CLOUD_API_KEY=your_api_key_from_step_1.5
WATSONX_PROJECT_ID=your_project_id_from_step_1.4
WATSONX_URL=https://us-south.ml.cloud.ibm.com
WATSONX_MODEL_ID=ibm/granite-3-8b-instruct

# Optional: Keep Gemini as fallback during migration
GEMINI_API_KEY=your_existing_gemini_key
USE_GRANITE=true
```

**Verification:**
```bash
# Check .env file is not tracked by git
git status | grep .env
# Should return nothing (file should be in .gitignore)
```

### Step 2.2: Install IBM watsonx SDK

**Action Steps:**
1. Update `requirements.txt`:

```txt
# Add these lines to requirements.txt
ibm-watsonx-ai>=1.0.0
ibm-cloud-sdk-core>=3.18.0
```

2. Install dependencies:

```bash
# Activate virtual environment
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/Mac

# Install new dependencies
pip install ibm-watsonx-ai ibm-cloud-sdk-core

# Verify installation
python -c "import ibm_watsonx_ai; print(ibm_watsonx_ai.__version__)"
```

**Expected Output:**
```
1.0.x  # or higher version
```

---

## Part 3: Create Granite Client Service (30 minutes)

### Step 3.1: Create Service Directory Structure

**Action Steps:**
```bash
# Create new service directory
mkdir -p services/watsonx_service
cd services/watsonx_service

# Create Python files
touch __init__.py
touch granite_client.py
touch main.py
touch config.py
```

### Step 3.2: Implement Granite Configuration

**File: `services/watsonx_service/config.py`**

```python
"""
Configuration for IBM watsonx.ai Granite client
"""
from pydantic import BaseModel
from typing import Optional
import os


class GraniteConfig(BaseModel):
    """Configuration for Granite LLM"""
    
    # IBM Cloud credentials
    api_key: str
    project_id: str
    url: str = "https://us-south.ml.cloud.ibm.com"
    
    # Model configuration
    model_id: str = "ibm/granite-3-8b-instruct"
    
    # Generation parameters
    max_new_tokens: int = 2048
    temperature: float = 0.7
    top_p: float = 0.9
    top_k: int = 50
    repetition_penalty: float = 1.1
    
    # Fallback configuration
    use_fallback: bool = True
    fallback_to_gemini: bool = False
    
    @classmethod
    def from_env(cls) -> "GraniteConfig":
        """Load configuration from environment variables"""
        return cls(
            api_key=os.getenv("IBM_CLOUD_API_KEY", ""),
            project_id=os.getenv("WATSONX_PROJECT_ID", ""),
            url=os.getenv("WATSONX_URL", "https://us-south.ml.cloud.ibm.com"),
            model_id=os.getenv("WATSONX_MODEL_ID", "ibm/granite-3-8b-instruct"),
            use_fallback=os.getenv("USE_GRANITE", "true").lower() == "true",
            fallback_to_gemini=os.getenv("FALLBACK_TO_GEMINI", "false").lower() == "true"
        )
    
    def validate_credentials(self) -> bool:
        """Validate that required credentials are present"""
        return bool(self.api_key and self.project_id)


# Global config instance
granite_config = GraniteConfig.from_env()
```

### Step 3.3: Implement Granite Client

**File: `services/watsonx_service/granite_client.py`**

```python
"""
IBM watsonx.ai Granite LLM Client
"""
from ibm_watsonx_ai.foundation_models import Model
from ibm_watsonx_ai.metanames import GenTextParamsMetaNames as GenParams
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from typing import Optional, Dict, Any
import logging
import json

from .config import granite_config

logger = logging.getLogger(__name__)


class GraniteClient:
    """Client for IBM watsonx.ai Granite models"""
    
    def __init__(self, config: Optional[Any] = None):
        """
        Initialize Granite client
        
        Args:
            config: Optional GraniteConfig instance. If None, uses global config.
        """
        self.config = config or granite_config
        
        if not self.config.validate_credentials():
            raise ValueError(
                "IBM watsonx credentials not configured. "
                "Set IBM_CLOUD_API_KEY and WATSONX_PROJECT_ID in .env"
            )
        
        # Initialize IBM watsonx.ai model
        self.model = self._initialize_model()
        logger.info(f"Granite client initialized with model: {self.config.model_id}")
    
    def _initialize_model(self) -> Model:
        """Initialize the Granite model"""
        try:
            model = Model(
                model_id=self.config.model_id,
                params={
                    GenParams.MAX_NEW_TOKENS: self.config.max_new_tokens,
                    GenParams.TEMPERATURE: self.config.temperature,
                    GenParams.TOP_P: self.config.top_p,
                    GenParams.TOP_K: self.config.top_k,
                    GenParams.REPETITION_PENALTY: self.config.repetition_penalty,
                },
                credentials={
                    "apikey": self.config.api_key,
                    "url": self.config.url
                },
                project_id=self.config.project_id
            )
            return model
        except Exception as e:
            logger.error(f"Failed to initialize Granite model: {str(e)}")
            raise
    
    def generate(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        max_tokens: Optional[int] = None,
        temperature: Optional[float] = None
    ) -> str:
        """
        Generate text using Granite model
        
        Args:
            prompt: User prompt
            system_prompt: Optional system prompt for context
            max_tokens: Override default max_new_tokens
            temperature: Override default temperature
            
        Returns:
            Generated text
        """
        try:
            # Construct full prompt with system context
            full_prompt = self._construct_prompt(prompt, system_prompt)
            
            # Override parameters if provided
            params = {}
            if max_tokens:
                params[GenParams.MAX_NEW_TOKENS] = max_tokens
            if temperature is not None:
                params[GenParams.TEMPERATURE] = temperature
            
            # Generate text
            logger.info(f"Generating with Granite (prompt length: {len(full_prompt)} chars)")
            
            if params:
                # Create temporary model with custom params
                temp_model = Model(
                    model_id=self.config.model_id,
                    params={**self.model.params, **params},
                    credentials={"apikey": self.config.api_key, "url": self.config.url},
                    project_id=self.config.project_id
                )
                response = temp_model.generate_text(prompt=full_prompt)
            else:
                response = self.model.generate_text(prompt=full_prompt)
            
            logger.info(f"Granite generation successful (response length: {len(response)} chars)")
            return response
            
        except Exception as e:
            logger.error(f"Granite generation failed: {str(e)}")
            raise
    
    def generate_structured(
        self,
        prompt: str,
        schema: Dict[str, Any],
        system_prompt: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Generate structured JSON output
        
        Args:
            prompt: User prompt
            schema: JSON schema for expected output
            system_prompt: Optional system prompt
            
        Returns:
            Parsed JSON object
        """
        try:
            # Add JSON schema instruction to prompt
            json_instruction = (
                f"\n\nRespond with valid JSON matching this schema:\n"
                f"```json\n{json.dumps(schema, indent=2)}\n```\n"
                f"Return ONLY the JSON object, no additional text."
            )
            
            full_prompt = prompt + json_instruction
            
            # Generate response
            response = self.generate(full_prompt, system_prompt)
            
            # Extract JSON from response (handle markdown code blocks)
            json_text = self._extract_json(response)
            
            # Parse JSON
            result = json.loads(json_text)
            logger.info("Structured generation successful")
            return result
            
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse JSON response: {str(e)}")
            logger.error(f"Response was: {response}")
            raise ValueError(f"Invalid JSON response from Granite: {str(e)}")
        except Exception as e:
            logger.error(f"Structured generation failed: {str(e)}")
            raise
    
    def _construct_prompt(self, prompt: str, system_prompt: Optional[str] = None) -> str:
        """Construct full prompt with system context"""
        if system_prompt:
            return f"{system_prompt}\n\n{prompt}"
        return prompt
    
    def _extract_json(self, text: str) -> str:
        """Extract JSON from text (handles markdown code blocks)"""
        # Remove markdown code blocks if present
        if "```json" in text:
            start = text.find("```json") + 7
            end = text.find("```", start)
            return text[start:end].strip()
        elif "```" in text:
            start = text.find("```") + 3
            end = text.find("```", start)
            return text[start:end].strip()
        return text.strip()
    
    def test_connection(self) -> bool:
        """Test connection to IBM watsonx.ai"""
        try:
            response = self.generate("Say 'Hello from Granite!'", max_tokens=50)
            return "Granite" in response or "Hello" in response
        except Exception as e:
            logger.error(f"Connection test failed: {str(e)}")
            return False


# Global client instance
_granite_client: Optional[GraniteClient] = None


def get_granite_client() -> GraniteClient:
    """Get or create global Granite client instance"""
    global _granite_client
    if _granite_client is None:
        _granite_client = GraniteClient()
    return _granite_client
```

### Step 3.4: Create Test Script

**File: `services/watsonx_service/test_granite.py`**

```python
"""
Test script for Granite client
"""
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.append(str(project_root))

from services.watsonx_service.granite_client import GraniteClient
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def test_basic_generation():
    """Test basic text generation"""
    print("\n" + "="*60)
    print("TEST 1: Basic Text Generation")
    print("="*60)
    
    client = GraniteClient()
    
    prompt = "Write a short introduction about artificial intelligence in 2-3 sentences."
    
    print(f"\nPrompt: {prompt}")
    print("\nGenerating...")
    
    response = client.generate(prompt)
    
    print(f"\nResponse:\n{response}")
    print("\n✓ Test passed!")


def test_system_prompt():
    """Test generation with system prompt"""
    print("\n" + "="*60)
    print("TEST 2: Generation with System Prompt")
    print("="*60)
    
    client = GraniteClient()
    
    system_prompt = "You are a professional blog writer with expertise in technology."
    prompt = "Write a blog introduction about cloud computing."
    
    print(f"\nSystem Prompt: {system_prompt}")
    print(f"User Prompt: {prompt}")
    print("\nGenerating...")
    
    response = client.generate(prompt, system_prompt=system_prompt)
    
    print(f"\nResponse:\n{response}")
    print("\n✓ Test passed!")


def test_structured_output():
    """Test structured JSON generation"""
    print("\n" + "="*60)
    print("TEST 3: Structured JSON Output")
    print("="*60)
    
    client = GraniteClient()
    
    prompt = "Create a blog post outline about machine learning."
    schema = {
        "title": "string",
        "sections": ["string"],
        "estimated_words": "number"
    }
    
    print(f"\nPrompt: {prompt}")
    print(f"Expected Schema: {schema}")
    print("\nGenerating...")
    
    response = client.generate_structured(prompt, schema)
    
    print(f"\nResponse:\n{response}")
    print("\n✓ Test passed!")


def test_connection():
    """Test connection to watsonx.ai"""
    print("\n" + "="*60)
    print("TEST 4: Connection Test")
    print("="*60)
    
    client = GraniteClient()
    
    print("\nTesting connection to IBM watsonx.ai...")
    
    success = client.test_connection()
    
    if success:
        print("\n✓ Connection successful!")
    else:
        print("\n✗ Connection failed!")
        sys.exit(1)


if __name__ == "__main__":
    try:
        test_connection()
        test_basic_generation()
        test_system_prompt()
        test_structured_output()
        
        print("\n" + "="*60)
        print("ALL TESTS PASSED! ✓")
        print("="*60)
        print("\nGranite client is ready to use!")
        
    except Exception as e:
        print(f"\n✗ Test failed: {str(e)}")
        sys.exit(1)
```

**Run the test:**
```bash
python services/watsonx_service/test_granite.py
```

**Expected Output:**
```
============================================================
TEST 4: Connection Test
============================================================

Testing connection to IBM watsonx.ai...

✓ Connection successful!

============================================================
TEST 1: Basic Text Generation
============================================================

Prompt: Write a short introduction about artificial intelligence in 2-3 sentences.

Generating...

Response:
Artificial intelligence (AI) is revolutionizing how we interact with technology...

✓ Test passed!

[... more tests ...]

============================================================
ALL TESTS PASSED! ✓
============================================================

Granite client is ready to use!
```

---

## Part 4: Replace Gemini with Granite (45 minutes)

### Step 4.1: Update Blog Service

**File: `services/blog_service/main.py`**

Find the Gemini import and generation code, then replace:

```python
# OLD CODE (Gemini):
# import google.generativeai as genai
# genai.configure(api_key=api_key)
# model = genai.GenerativeModel('gemini-pro')
# response = model.generate_content(prompt)
# content = response.text

# NEW CODE (Granite):
from services.watsonx_service.granite_client import get_granite_client

# Get Granite client
granite = get_granite_client()

# Generate content
system_prompt = """You are a professional blog writer with expertise in creating 
engaging, well-structured content. Write in a clear, accessible style with proper 
formatting and SEO optimization."""

response = granite.generate(
    prompt=user_prompt,
    system_prompt=system_prompt,
    max_tokens=2048,
    temperature=0.7
)

content = response
```

### Step 4.2: Update Generation Endpoint

**Locate the `/api/blogs/{blog_id}/generate` endpoint and update:**

```python
@app.post("/blogs/{blog_id}/generate")
async def generate_blog_content(
    blog_id: str,
    request: dict,
    api_key: str = Depends(get_current_api_key)
):
    """Generate blog content using IBM Granite"""
    try:
        prompt = request.get("prompt", "")
        generation_type = request.get("generation_type", "all")
        
        # Get Granite client
        granite = get_granite_client()
        
        # Construct system prompt based on generation type
        if generation_type == "content":
            system_prompt = """You are a professional blog content writer. 
            Create engaging, well-structured blog content with proper headings, 
            paragraphs, and formatting."""
        elif generation_type == "title":
            system_prompt = """You are an expert at creating compelling blog titles. 
            Create a catchy, SEO-friendly title."""
        else:  # all
            system_prompt = """You are a professional blog writer. Create a complete 
            blog post with title, introduction, body content, and conclusion."""
        
        # Generate content
        logger.info(f"Generating content for blog {blog_id} using Granite")
        content = granite.generate(
            prompt=prompt,
            system_prompt=system_prompt,
            max_tokens=2048,
            temperature=0.7
        )
        
        # Save content (existing logic)
        # ... rest of your code ...
        
        return {
            "success": True,
            "message": "Content generated successfully with IBM Granite",
            "data": {
                "blog_id": blog_id,
                "content": content,
                "model": "ibm/granite-3-8b-instruct"
            }
        }
        
    except Exception as e:
        logger.error(f"Generation failed: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
```

### Step 4.3: Add Fallback Logic (Optional)

**For safety during migration, add Gemini fallback:**

```python
def generate_with_fallback(prompt: str, system_prompt: str = None) -> str:
    """Generate content with Granite, fallback to Gemini if needed"""
    try:
        # Try Granite first
        granite = get_granite_client()
        return granite.generate(prompt, system_prompt)
    except Exception as e:
        logger.warning(f"Granite failed: {str(e)}, falling back to Gemini")
        
        # Fallback to Gemini
        if granite_config.fallback_to_gemini:
            import google.generativeai as genai
            genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
            model = genai.GenerativeModel('gemini-pro')
            response = model.generate_content(prompt)
            return response.text
        else:
            raise
```

---

## Part 5: Testing & Verification (15 minutes)

### Step 5.1: Test Blog Generation

**Action Steps:**
1. Start all services:
```bash
python start_all_services.py
```

2. Open browser: http://localhost:8003

3. Create a new blog:
   - Title: "Test IBM Granite Integration"
   - Prompt: "Write about the benefits of AI in healthcare"
   - Click "Generate"

4. Verify:
   - Content is generated successfully
   - Quality is comparable to Gemini
   - Response time is acceptable (5-10 seconds)

### Step 5.2: Check Logs

**Look for Granite-specific log messages:**
```
INFO: Granite client initialized with model: ibm/granite-3-8b-instruct
INFO: Generating with Granite (prompt length: 156 chars)
INFO: Granite generation successful (response length: 1240 chars)
```

### Step 5.3: Compare Output Quality

**Create comparison test:**
```python
# test_comparison.py
from services.watsonx_service.granite_client import get_granite_client

granite = get_granite_client()

prompt = "Write a blog introduction about cloud computing in 3 paragraphs."

print("Generating with Granite...")
granite_output = granite.generate(prompt)

print("\n" + "="*60)
print("GRANITE OUTPUT:")
print("="*60)
print(granite_output)
```

---

## Success Criteria

### ✅ Module Complete When:
1. IBM watsonx.ai instance is active and accessible
2. Granite client successfully generates text
3. All test scripts pass
4. Blog service uses Granite instead of Gemini
5. Blog generation works end-to-end
6. Output quality meets expectations

### 📊 Metrics to Track:
- **Response Time**: 5-10 seconds per generation
- **Success Rate**: >95% successful generations
- **Cost**: ~$0.50 per 1M tokens (track in IBM Cloud dashboard)
- **Quality**: Subjective assessment of output coherence

---

## Troubleshooting

### Issue: "Invalid API key"
**Solution:**
```bash
# Verify API key in .env
cat .env | grep IBM_CLOUD_API_KEY

# Test API key
python -c "from services.watsonx_service.granite_client import GraniteClient; GraniteClient().test_connection()"
```

### Issue: "Project ID not found"
**Solution:**
1. Go to watsonx.ai platform
2. Click on your project
3. Copy PROJECT_ID from URL
4. Update .env file

### Issue: "Model not available"
**Solution:**
```bash
# Verify model ID
# Should be: ibm/granite-3-8b-instruct
# Check in Prompt Lab > View all foundation models
```

### Issue: "Slow response times"
**Solution:**
- Check region (Dallas/us-south is fastest for US)
- Reduce max_new_tokens if generating too much text
- Consider upgrading from Lite plan if hitting rate limits

---

## Next Steps

After completing this module, you can proceed to:
- **Enhancement 1-B**: Research Agent Implementation
- **Enhancement 1-C**: Writer Agent Implementation
- **Enhancement 1-D**: Reviewer Agent with Self-Correction Loop

This module provides the foundation for all subsequent agent implementations.