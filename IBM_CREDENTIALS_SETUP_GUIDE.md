# IBM Cloud Credentials Setup - Complete Step-by-Step Guide

## Overview
This guide shows you exactly how to get each credential needed for your `.env` file.

---

## Step 1: Get IBM_CLOUD_API_KEY

### Method 1: From IBM Cloud Dashboard (Recommended)

**Steps:**
1. Log into IBM Cloud: https://cloud.ibm.com/
2. Click on your **profile icon** (top right corner)
3. Select **"Profile and settings"** from dropdown
4. In the left sidebar, click **"API keys"**
5. Click **"Create +"** button (blue button on right)
6. Fill in the form:
   ```
   Name: BlogAgent-Hackathon-Key
   Description: API key for IBM Bob Hackathon - BlogAgent Pro
   ```
7. Click **"Create"**
8. **CRITICAL:** A popup appears with your API key
   - Click **"Copy"** button immediately
   - Save it somewhere safe (you'll only see it once!)
   - Example format: `xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx`

**Screenshot Checkpoints:**
- ✓ You see "API keys" page with list of keys
- ✓ New key appears in the list
- ✓ Key is copied to clipboard

**What to do:**
```bash
# Add to .env file
IBM_CLOUD_API_KEY=paste_your_copied_key_here
```

### Method 2: From Hackathon Organizers

If you're in a hackathon with pre-provisioned services:

1. Check your hackathon welcome email
2. Look for "IBM Cloud Credentials" section
3. Copy the API key provided
4. If not provided, ask hackathon organizers in Slack/Discord

---

## Step 2: Get WATSONX_PROJECT_ID

### Create New watsonx.ai Project

**Steps:**

1. **Navigate to watsonx.ai Platform**
   - URL: https://dataplatform.cloud.ibm.com/
   - Or from IBM Cloud dashboard: Search for "watsonx.ai" → Click "Launch watsonx.ai"

2. **Create New Project**
   - Click **"Projects"** in left sidebar
   - Click **"New project"** button (top right)
   - Select **"Create an empty project"**

3. **Configure Project**
   ```
   Name: BlogAgent-Hackathon
   Description: AI-powered blog generation with autonomous agents for IBM Bob Hackathon
   ```

4. **Select Storage**
   - Under "Select storage service"
   - Choose **"watsonx-Hackathon COS"** from dropdown
   - (This is your pre-provisioned Cloud Object Storage)
   - If you don't see it, click "Refresh" or contact organizers

5. **Create Project**
   - Click **"Create"** button
   - Wait 10-20 seconds for project creation

6. **Get PROJECT_ID**
   - After creation, you'll be redirected to project page
   - Look at the URL in your browser
   - Format: `https://dataplatform.cloud.ibm.com/projects/{PROJECT_ID}?context=wx`
   - Copy the PROJECT_ID from the URL
   - Example: `12345678-abcd-1234-efgh-123456789012`

**Visual Guide:**
```
URL: https://dataplatform.cloud.ibm.com/projects/12345678-abcd-1234-efgh-123456789012?context=wx
                                                    ↑
                                            This is your PROJECT_ID
```

**What to do:**
```bash
# Add to .env file
WATSONX_PROJECT_ID=12345678-abcd-1234-efgh-123456789012
```

**Verification:**
- Go back to Projects list
- You should see "BlogAgent-Hackathon" project
- Click on it to confirm it opens

---

## Step 3: Get WATSONX_URL

### This is Standard - No Configuration Needed

The watsonx.ai URL depends on your region. For most hackathons:

**US South (Dallas) - Most Common:**
```bash
WATSONX_URL=https://us-south.ml.cloud.ibm.com
```

**Other Regions (if applicable):**
```bash
# US East (Washington DC)
WATSONX_URL=https://us-east.ml.cloud.ibm.com

# EU (Frankfurt)
WATSONX_URL=https://eu-de.ml.cloud.ibm.com

# EU (London)
WATSONX_URL=https://eu-gb.ml.cloud.ibm.com

# Asia Pacific (Tokyo)
WATSONX_URL=https://jp-tok.ml.cloud.ibm.com
```

**How to Verify Your Region:**

1. In IBM Cloud dashboard: https://cloud.ibm.com/
2. Look at your services list
3. Find "watsonx-Hackathon COS" or any service
4. Click on it
5. Look for "Region" field
6. Use corresponding URL above

**Most likely for hackathon:**
```bash
# Add to .env file
WATSONX_URL=https://us-south.ml.cloud.ibm.com
```

---

## Step 4: Get WATSONX_MODEL_ID

### Verify Granite Model Access

**Steps:**

1. **Open Your Project**
   - Go to: https://dataplatform.cloud.ibm.com/
   - Click on "BlogAgent-Hackathon" project

2. **Access Prompt Lab**
   - In left sidebar, click **"Prompt Lab"**
   - Or click **"Work with foundation models"** button

3. **View Available Models**
   - Click **"View all foundation models"** link
   - Scroll through the list
   - Look for **"Granite"** models

4. **Find Granite 3.3 8B Instruct**
   - Look for: **"granite-3-8b-instruct"**
   - Or: **"ibm/granite-3-8b-instruct"**
   - Click on it to see details

5. **Verify Model ID**
   - Model ID format: `ibm/granite-3-8b-instruct`
   - This is the exact string you need

**Standard Model ID (No Configuration Needed):**
```bash
# Add to .env file
WATSONX_MODEL_ID=ibm/granite-3-8b-instruct
```

**Alternative Granite Models (if 3.3 8B not available):**
```bash
# Granite 3.0 8B Instruct
WATSONX_MODEL_ID=ibm/granite-3.0-8b-instruct

# Granite 13B Instruct (larger, slower)
WATSONX_MODEL_ID=ibm/granite-13b-instruct-v2

# Granite 20B (if available)
WATSONX_MODEL_ID=ibm/granite-20b-multilingual
```

**Test Model Access:**

1. In Prompt Lab, select the model
2. Type a test prompt: "Write a short sentence about AI"
3. Click "Generate"
4. If you get a response, the model is accessible
5. If you get an error, try a different Granite model

---

## Complete .env File Template

After collecting all credentials, create `.env` file in project root:

```bash
# ============================================
# IBM CLOUD AUTHENTICATION
# ============================================
IBM_CLOUD_API_KEY=your_api_key_from_step_1

# ============================================
# WATSONX.AI CONFIGURATION
# ============================================
WATSONX_PROJECT_ID=your_project_id_from_step_2
WATSONX_URL=https://us-south.ml.cloud.ibm.com
WATSONX_MODEL_ID=ibm/granite-3-8b-instruct

# ============================================
# CLOUD OBJECT STORAGE (COS)
# ============================================
COS_INSTANCE_ID=watsonx-Hackathon_COS
COS_API_KEY=${IBM_CLOUD_API_KEY}
COS_ENDPOINT=https://s3.us-south.cloud-object-storage.appdomain.cloud
COS_BUCKET=blogagent-storage

# ============================================
# ORCHESTRATE
# ============================================
ORCHESTRATE_INSTANCE_ID=watsonx-Hackathon_Orchestrate
ORCHESTRATE_API_KEY=${IBM_CLOUD_API_KEY}
ORCHESTRATE_URL=https://orchestrate.watsonx.ibm.com

# ============================================
# NATURAL LANGUAGE UNDERSTANDING (NLU)
# ============================================
NLU_INSTANCE_ID=watsonx-Hackathon_NLU
NLU_API_KEY=${IBM_CLOUD_API_KEY}
NLU_URL=https://api.us-south.natural-language-understanding.watson.cloud.ibm.com

# ============================================
# CLOUDANT DATABASE
# ============================================
CLOUDANT_INSTANCE_ID=watsonx-Hackathon_Cloudant
CLOUDANT_API_KEY=${IBM_CLOUD_API_KEY}
CLOUDANT_URL=https://your-account.cloudantnosqldb.appdomain.cloud
CLOUDANT_ACCOUNT=your-cloudant-account
CLOUDANT_DATABASE=pipeline_history

# ============================================
# GOVERNANCE
# ============================================
GOV_INSTANCE_ID=watsonx-Hackathon_GOV
GOV_API_KEY=${IBM_CLOUD_API_KEY}
GOV_URL=https://api.dataplatform.cloud.ibm.com/v2/governance

# ============================================
# APPLICATION SETTINGS
# ============================================
LOG_LEVEL=INFO
MAX_ITERATIONS=3
QUALITY_THRESHOLD=7.0
```

---

## Verification Steps

### Test Your Credentials

Create `test_credentials.py`:

```python
import os
from dotenv import load_dotenv

# Load .env file
load_dotenv()

print("Testing IBM Cloud Credentials...\n")

# Test 1: API Key
api_key = os.getenv("IBM_CLOUD_API_KEY")
if api_key and len(api_key) > 20:
    print("✓ IBM_CLOUD_API_KEY: Found (length: {})".format(len(api_key)))
else:
    print("✗ IBM_CLOUD_API_KEY: Missing or invalid")

# Test 2: Project ID
project_id = os.getenv("WATSONX_PROJECT_ID")
if project_id and len(project_id) == 36:  # UUID format
    print("✓ WATSONX_PROJECT_ID: Found ({})".format(project_id[:8] + "..."))
else:
    print("✗ WATSONX_PROJECT_ID: Missing or invalid format")

# Test 3: URL
url = os.getenv("WATSONX_URL")
if url and "ml.cloud.ibm.com" in url:
    print("✓ WATSONX_URL: Valid ({})".format(url))
else:
    print("✗ WATSONX_URL: Missing or invalid")

# Test 4: Model ID
model_id = os.getenv("WATSONX_MODEL_ID")
if model_id and "granite" in model_id.lower():
    print("✓ WATSONX_MODEL_ID: Valid ({})".format(model_id))
else:
    print("✗ WATSONX_MODEL_ID: Missing or invalid")

print("\n" + "="*50)
print("Credential check complete!")
print("="*50)
```

Run:
```bash
python test_credentials.py
```

Expected output:
```
Testing IBM Cloud Credentials...

✓ IBM_CLOUD_API_KEY: Found (length: 44)
✓ WATSONX_PROJECT_ID: Found (12345678...)
✓ WATSONX_URL: Valid (https://us-south.ml.cloud.ibm.com)
✓ WATSONX_MODEL_ID: Valid (ibm/granite-3-8b-instruct)

==================================================
Credential check complete!
==================================================
```

---

## Test Granite Connection

Create `test_granite_connection.py`:

```python
import os
from dotenv import load_dotenv
from ibm_watsonx_ai.foundation_models import Model
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

# Load environment
load_dotenv()

print("Testing Granite Model Connection...\n")

try:
    # Initialize model
    model = Model(
        model_id=os.getenv("WATSONX_MODEL_ID"),
        params={
            "max_new_tokens": 100,
            "temperature": 0.7
        },
        credentials={
            "apikey": os.getenv("IBM_CLOUD_API_KEY"),
            "url": os.getenv("WATSONX_URL")
        },
        project_id=os.getenv("WATSONX_PROJECT_ID")
    )
    
    print("✓ Model initialized successfully")
    
    # Test generation
    print("\nTesting generation with prompt: 'Hello, Granite!'")
    response = model.generate_text(prompt="Hello, Granite! Respond with a short greeting.")
    
    print("\n" + "="*50)
    print("RESPONSE FROM GRANITE:")
    print("="*50)
    print(response)
    print("="*50)
    
    print("\n✓ SUCCESS! Granite is working correctly!")
    
except Exception as e:
    print(f"\n✗ ERROR: {str(e)}")
    print("\nTroubleshooting:")
    print("1. Check your IBM_CLOUD_API_KEY is correct")
    print("2. Verify WATSONX_PROJECT_ID matches your project")
    print("3. Ensure you have access to Granite models in your project")
    print("4. Check WATSONX_URL matches your region")
```

Run:
```bash
pip install ibm-watsonx-ai ibm-cloud-sdk-core python-dotenv
python test_granite_connection.py
```

Expected output:
```
Testing Granite Model Connection...

✓ Model initialized successfully

Testing generation with prompt: 'Hello, Granite!'

==================================================
RESPONSE FROM GRANITE:
==================================================
Hello! I'm Granite, an AI assistant. How can I help you today?
==================================================

✓ SUCCESS! Granite is working correctly!
```

---

## Troubleshooting

### Issue: "Invalid API Key"
**Solution:**
1. Go back to IBM Cloud → Profile → API keys
2. Delete old key
3. Create new key
4. Copy immediately and update .env

### Issue: "Project not found"
**Solution:**
1. Go to https://dataplatform.cloud.ibm.com/
2. Click Projects
3. Verify "BlogAgent-Hackathon" exists
4. Click on it and copy PROJECT_ID from URL again

### Issue: "Model not available"
**Solution:**
1. In Prompt Lab, click "View all foundation models"
2. Check which Granite models you can access
3. Use the exact model ID shown
4. Try alternative: `ibm/granite-3.0-8b-instruct`

### Issue: "Region mismatch"
**Solution:**
1. Check your COS service region in IBM Cloud
2. Update WATSONX_URL to match that region
3. Common: us-south, us-east, eu-de, eu-gb

---

## Quick Reference Card

Print this and keep it handy:

```
┌─────────────────────────────────────────────────┐
│  IBM CLOUD CREDENTIALS QUICK REFERENCE          │
├─────────────────────────────────────────────────┤
│                                                 │
│  1. API KEY                                     │
│     Where: cloud.ibm.com → Profile → API keys  │
│     Format: 44 characters                       │
│                                                 │
│  2. PROJECT ID                                  │
│     Where: dataplatform.cloud.ibm.com → URL    │
│     Format: UUID (36 chars with dashes)         │
│                                                 │
│  3. WATSONX URL                                 │
│     US South: us-south.ml.cloud.ibm.com        │
│     US East: us-east.ml.cloud.ibm.com          │
│                                                 │
│  4. MODEL ID                                    │
│     Standard: ibm/granite-3-8b-instruct        │
│     Where: Prompt Lab → View all models        │
│                                                 │
└─────────────────────────────────────────────────┘
```

---

## Next Steps

After getting all credentials:

1. ✅ Create `.env` file with all values
2. ✅ Run `python test_credentials.py`
3. ✅ Run `python test_granite_connection.py`
4. ✅ If all tests pass, proceed to Enhancement 1-A
5. ✅ Start building your agentic blog system!

---

## Support

If you're stuck:
1. Check IBM Cloud status: https://cloud.ibm.com/status
2. Review IBM watsonx.ai docs: https://cloud.ibm.com/docs/watsonx
3. Contact hackathon organizers
4. Check hackathon Slack/Discord for help

Good luck with your hackathon! 🚀