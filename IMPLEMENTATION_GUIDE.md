# Implementation Guide - Enhancement 1-A: IBM watsonx Foundation

## What We've Done So Far

✅ **Updated .env.example** - Configured for IBM watsonx services instead of Gemini
✅ **Updated requirements.txt** - Added IBM watsonx.ai and related dependencies
✅ **Created watsonx_service/** - New service directory structure
✅ **Implemented GraniteConfig** - Configuration management for Granite models
✅ **Implemented GraniteClient** - Full-featured Granite LLM client
✅ **Created test_granite.py** - Comprehensive test suite

## Next Steps for You

### Step 1: Get Your IBM Credentials (15-20 minutes)

Follow the detailed guide in **IBM_CREDENTIALS_SETUP_GUIDE.md** to get:

1. **IBM_CLOUD_API_KEY** - From IBM Cloud Dashboard → Profile → API keys
2. **WATSONX_PROJECT_ID** - Create project at dataplatform.cloud.ibm.com
3. **WATSONX_URL** - Usually `https://us-south.ml.cloud.ibm.com`
4. **WATSONX_MODEL_ID** - Usually `ibm/granite-3-8b-instruct`

### Step 2: Create Your .env File (5 minutes)

```bash
# Copy the example file
cp .env.example .env

# Edit .env and add your credentials
# Use any text editor (VS Code, Notepad, etc.)
```

**Minimum required configuration:**
```bash
# IBM Cloud Authentication
IBM_CLOUD_API_KEY=your_actual_api_key_here

# watsonx.ai Configuration
WATSONX_PROJECT_ID=your_actual_project_id_here
WATSONX_URL=https://us-south.ml.cloud.ibm.com
WATSONX_MODEL_ID=ibm/granite-3-8b-instruct

# Security
SECRET_KEY=generate_using_python_secrets_module
```

### Step 3: Install Dependencies (5-10 minutes)

```bash
# Make sure you're in the project root directory
cd c:/workspace/ForgeByBob

# Activate your virtual environment (if you have one)
# venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/Mac

# Install all dependencies
pip install -r requirements.txt
```

**Expected output:**
```
Successfully installed ibm-watsonx-ai-1.x.x ibm-cloud-sdk-core-3.x.x ...
```

### Step 4: Test Granite Connection (5 minutes)

```bash
# Run the test script
python services/watsonx_service/test_granite.py
```

**Expected output:**
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

### Step 5: Verify Everything Works

Create a simple test file `test_quick.py`:

```python
from services.watsonx_service import get_granite_client

# Get Granite client
granite = get_granite_client()

# Test generation
response = granite.generate("Write a haiku about AI")

print("Granite Response:")
print(response)
```

Run it:
```bash
python test_quick.py
```

## Troubleshooting

### Issue: "IBM watsonx credentials not configured"

**Solution:**
1. Check your `.env` file exists in project root
2. Verify `IBM_CLOUD_API_KEY` and `WATSONX_PROJECT_ID` are set
3. Make sure there are no extra spaces or quotes around values

### Issue: "Import ibm_watsonx_ai could not be resolved"

**Solution:**
```bash
# Install the package explicitly
pip install ibm-watsonx-ai ibm-cloud-sdk-core

# Verify installation
python -c "import ibm_watsonx_ai; print('Success!')"
```

### Issue: "Project not found" or "Invalid project ID"

**Solution:**
1. Go to https://dataplatform.cloud.ibm.com/
2. Click on your project
3. Copy the PROJECT_ID from the URL (36-character UUID)
4. Update `.env` file with correct PROJECT_ID

### Issue: "Model not available"

**Solution:**
1. In watsonx.ai, go to Prompt Lab
2. Click "View all foundation models"
3. Find which Granite models you have access to
4. Update `WATSONX_MODEL_ID` in `.env` with the correct model ID

## What's Next?

After completing Enhancement 1-A, you can proceed to:

### Enhancement 1-B: Orchestration Framework
- Set up agent coordination
- Create base agent classes
- Implement simple 2-agent pipeline

### Enhancement 1-C: Research Agent
- Add web search capabilities
- Implement source credibility assessment
- Create 3-agent pipeline

### Enhancement 1-D: Self-Correction Loop
- Implement Reviewer Agent
- Add autonomous quality improvement
- Create 4-agent pipeline with feedback loop

### Enhancement 1-E: Real-time Dashboard
- Build SSE-powered dashboard
- Add real-time agent status tracking
- Create demo-ready visualization

## Current Project Structure

```
ForgeByBob/
├── .env                          # Your credentials (DO NOT COMMIT)
├── .env.example                  # Template (updated for IBM)
├── requirements.txt              # Dependencies (updated for IBM)
├── IBM_CREDENTIALS_SETUP_GUIDE.md
├── HACKATHON_SERVICES_SETUP.md
├── IMPLEMENTATION_GUIDE.md       # This file
├── services/
│   ├── watsonx_service/          # NEW: IBM watsonx service
│   │   ├── __init__.py
│   │   ├── config.py             # Granite configuration
│   │   ├── granite_client.py     # Granite LLM client
│   │   ├── test_granite.py       # Test suite
│   │   └── main.py               # (Future: FastAPI service)
│   ├── blog_service/             # Existing (will update next)
│   ├── settings_service/         # Existing
│   ├── ui_service/               # Existing
│   └── api_gateway/              # Existing
└── shared/
    ├── config.py                 # Existing (will update next)
    └── ...
```

## Success Criteria

You've successfully completed Enhancement 1-A when:

- ✅ `.env` file is configured with IBM credentials
- ✅ All dependencies are installed
- ✅ `test_granite.py` passes all tests
- ✅ You can generate text using Granite client
- ✅ No import errors in VS Code

## Time Estimate

- **Setup**: 30-40 minutes
- **Testing**: 10-15 minutes
- **Total**: ~1 hour

## Support

If you get stuck:
1. Check **IBM_CREDENTIALS_SETUP_GUIDE.md** for credential issues
2. Check **HACKATHON_SERVICES_SETUP.md** for service configuration
3. Review error messages carefully
4. Contact hackathon organizers if IBM services are not accessible

## Ready to Continue?

Once Enhancement 1-A is working, let me know and I'll help you:
1. Update the existing blog service to use Granite instead of Gemini
2. Implement Enhancement 1-B (Orchestration Framework)
3. Continue with the remaining enhancements

Good luck! 🚀