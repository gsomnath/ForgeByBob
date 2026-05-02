# IBM Hackathon Services Configuration Guide

## Available Services

You have the following IBM services provisioned for the hackathon:

1. **watsonx-Hackathon Cloudant** - NoSQL database
2. **watsonx-Hackathon COS** - Cloud Object Storage
3. **watsonx-Hackathon GOV** - Governance and compliance
4. **watsonx-Hackathon NLU** - Natural Language Understanding
5. **watsonx-Hackathon Orchestrate** - Agent orchestration

## Service Mapping to Enhancements

### Enhancement 1-A: IBM watsonx Foundation
**Primary Services:**
- **watsonx.ai Platform** (access via dataplatform.cloud.ibm.com)
- **watsonx-Hackathon COS** - For project storage

**Configuration:**
```bash
# .env configuration
IBM_CLOUD_API_KEY=<your_hackathon_api_key>
WATSONX_PROJECT_ID=<project_id_from_new_project>
WATSONX_URL=https://us-south.ml.cloud.ibm.com
WATSONX_MODEL_ID=ibm/granite-3-8b-instruct

# Cloud Object Storage
COS_INSTANCE_ID=<watsonx-Hackathon_COS_instance_id>
COS_API_KEY=<same_as_IBM_CLOUD_API_KEY>
COS_ENDPOINT=https://s3.us-south.cloud-object-storage.appdomain.cloud
```

**Setup Steps:**
1. Go to https://dataplatform.cloud.ibm.com/
2. Create new project: "BlogAgent-Hackathon"
3. Select **watsonx-Hackathon COS** as storage
4. Copy PROJECT_ID from URL
5. Access Granite models via Prompt Lab

---

### Enhancement 1-B: Orchestration Framework
**Primary Services:**
- **watsonx-Hackathon Orchestrate** - Agent coordination

**Configuration:**
```bash
# .env configuration
ORCHESTRATE_INSTANCE_ID=<watsonx-Hackathon_Orchestrate_id>
ORCHESTRATE_API_KEY=<same_as_IBM_CLOUD_API_KEY>
ORCHESTRATE_URL=https://orchestrate.watsonx.ibm.com
```

**Setup Steps:**
1. Access Orchestrate via IBM Cloud dashboard
2. Create workspace: "BlogAgent-Orchestration"
3. Connect to watsonx.ai project
4. Define agent skills (research, writer, reviewer, publisher)

**Update to Enhancement 1-B:**
- Replace lightweight orchestration with full IBM Orchestrate
- Use Orchestrate's built-in agent coordination
- Leverage Orchestrate's skill management

---

### Enhancement 1-C: Research Agent
**Primary Services:**
- **watsonx-Hackathon NLU** - Enhanced text analysis
- **watsonx.ai** - Granite models

**Configuration:**
```bash
# .env configuration
NLU_INSTANCE_ID=<watsonx-Hackathon_NLU_id>
NLU_API_KEY=<same_as_IBM_CLOUD_API_KEY>
NLU_URL=https://api.us-south.natural-language-understanding.watson.cloud.ibm.com
```

**Enhanced Features with NLU:**
- Source credibility analysis using NLU sentiment
- Entity extraction from research sources
- Keyword extraction for SEO optimization
- Concept analysis for topic relevance

**Update to Enhancement 1-C:**
```python
# Add NLU integration to research agent
from ibm_watson import NaturalLanguageUnderstandingV1
from ibm_watson.natural_language_understanding_v1 import Features, EntitiesOptions, KeywordsOptions

class ResearchAgent(BaseAgent):
    def __init__(self):
        super().__init__()
        self.nlu = NaturalLanguageUnderstandingV1(
            version='2022-04-07',
            authenticator=IAMAuthenticator(os.getenv('NLU_API_KEY'))
        )
        self.nlu.set_service_url(os.getenv('NLU_URL'))
    
    async def _analyze_source_with_nlu(self, text: str):
        """Analyze source using Watson NLU"""
        response = self.nlu.analyze(
            text=text,
            features=Features(
                entities=EntitiesOptions(sentiment=True, limit=10),
                keywords=KeywordsOptions(sentiment=True, limit=10)
            )
        ).get_result()
        
        return {
            'entities': response.get('entities', []),
            'keywords': response.get('keywords', []),
            'sentiment': response.get('sentiment', {})
        }
```

---

### Enhancement 1-D: Reviewer Agent with Self-Correction
**Primary Services:**
- **watsonx.ai** - Granite models for evaluation
- **watsonx-Hackathon Orchestrate** - Loop management

**Configuration:**
```bash
# Uses existing watsonx.ai and Orchestrate configs
```

**Update to Enhancement 1-D:**
- Use Orchestrate's built-in loop conditions
- Define loop logic in Orchestrate workspace
- Leverage Orchestrate's state management

---

### Enhancement 1-E: Real-time Dashboard
**Primary Services:**
- **watsonx-Hackathon Cloudant** - Store pipeline history
- **watsonx-Hackathon Orchestrate** - Real-time events

**Configuration:**
```bash
# .env configuration
CLOUDANT_INSTANCE_ID=<watsonx-Hackathon_Cloudant_id>
CLOUDANT_API_KEY=<same_as_IBM_CLOUD_API_KEY>
CLOUDANT_URL=<cloudant_service_url>
CLOUDANT_DATABASE=pipeline_history
```

**Enhanced Features with Cloudant:**
- Persistent pipeline execution history
- Historical performance metrics
- Iteration comparison across runs
- Long-term analytics

**Update to Enhancement 1-E:**
```python
# Add Cloudant integration
from cloudant.client import Cloudant

class PipelineHistoryStore:
    def __init__(self):
        self.client = Cloudant.iam(
            account_name=os.getenv('CLOUDANT_ACCOUNT'),
            api_key=os.getenv('CLOUDANT_API_KEY'),
            connect=True
        )
        self.db = self.client['pipeline_history']
    
    def save_pipeline_execution(self, pipeline_data):
        """Save pipeline execution to Cloudant"""
        doc = {
            'pipeline_id': pipeline_data['pipeline_id'],
            'timestamp': datetime.utcnow().isoformat(),
            'iterations': pipeline_data['iteration_history'],
            'final_scores': pipeline_data['final_scores'],
            'duration': pipeline_data['duration_seconds']
        }
        self.db.create_document(doc)
```

---

### Enhancement 2: Trust & Governance Layer
**Primary Services:**
- **watsonx-Hackathon GOV** - Governance and compliance
- **watsonx.ai** - Granite self-evaluation

**Configuration:**
```bash
# .env configuration
GOV_INSTANCE_ID=<watsonx-Hackathon_GOV_id>
GOV_API_KEY=<same_as_IBM_CLOUD_API_KEY>
GOV_URL=https://api.dataplatform.cloud.ibm.com/v2/governance
```

**Enhanced Features with GOV:**
- Automated compliance checking
- Audit trail management
- Policy enforcement
- Risk assessment

**Update to Enhancement 2:**
```python
# Add Governance integration
from ibm_watson_openscale import APIClient

class GovernanceLayer:
    def __init__(self):
        self.gov_client = APIClient(
            authenticator=IAMAuthenticator(os.getenv('GOV_API_KEY'))
        )
        self.gov_client.set_service_url(os.getenv('GOV_URL'))
    
    async def log_content_evaluation(self, blog_id, trust_score):
        """Log evaluation to governance system"""
        self.gov_client.log_evaluation({
            'asset_id': blog_id,
            'evaluation_type': 'content_quality',
            'scores': trust_score,
            'timestamp': datetime.utcnow().isoformat()
        })
    
    async def check_compliance(self, content):
        """Check content against compliance policies"""
        return self.gov_client.check_compliance({
            'content': content,
            'policies': ['content_safety', 'brand_guidelines']
        })
```

---

## Updated Implementation Priority

### Phase 1: Core Foundation (4-5 hours)
**Services: watsonx.ai + COS**

1. Create watsonx.ai project with COS storage
2. Implement Granite client (Enhancement 1-A)
3. Test basic content generation
4. Verify API connectivity

**Deliverable:** Working Granite-powered blog generation

---

### Phase 2: Agent Orchestration (3-4 hours)
**Services: Orchestrate + watsonx.ai**

1. Set up Orchestrate workspace
2. Define agent skills in Orchestrate
3. Implement Writer and Publisher agents
4. Test 2-agent pipeline

**Deliverable:** Basic orchestrated workflow

---

### Phase 3: Enhanced Research (2-3 hours)
**Services: NLU + watsonx.ai**

1. Integrate Watson NLU
2. Implement Research Agent with NLU analysis
3. Add entity and keyword extraction
4. Test 3-agent pipeline

**Deliverable:** Research-backed content generation

---

### Phase 4: Self-Correction Loop (2-3 hours)
**Services: Orchestrate + watsonx.ai**

1. Implement Reviewer Agent
2. Configure loop conditions in Orchestrate
3. Test self-correction iterations
4. Verify quality improvements

**Deliverable:** Autonomous quality improvement (KEY DIFFERENTIATOR)

---

### Phase 5: Dashboard & Persistence (2-3 hours)
**Services: Cloudant + Orchestrate**

1. Set up Cloudant database
2. Implement pipeline history storage
3. Create real-time dashboard
4. Add historical analytics

**Deliverable:** Demo-ready visualization

---

### Phase 6: Governance Layer (1-2 hours)
**Services: GOV + watsonx.ai**

1. Integrate Governance service
2. Add compliance checking
3. Implement audit trails
4. Create governance dashboard

**Deliverable:** Enterprise-grade governance

---

## Total Implementation Time

**Minimum Viable Demo:** Phases 1-4 = 11-15 hours
**Full Implementation:** All Phases = 14-20 hours

---

## Environment Configuration Template

Create `.env` file with all services:

```bash
# IBM Cloud Authentication
IBM_CLOUD_API_KEY=<your_hackathon_api_key>

# watsonx.ai
WATSONX_PROJECT_ID=<BlogAgent-Hackathon_project_id>
WATSONX_URL=https://us-south.ml.cloud.ibm.com
WATSONX_MODEL_ID=ibm/granite-3-8b-instruct

# Cloud Object Storage
COS_INSTANCE_ID=<watsonx-Hackathon_COS_id>
COS_API_KEY=${IBM_CLOUD_API_KEY}
COS_ENDPOINT=https://s3.us-south.cloud-object-storage.appdomain.cloud
COS_BUCKET=blogagent-storage

# Orchestrate
ORCHESTRATE_INSTANCE_ID=<watsonx-Hackathon_Orchestrate_id>
ORCHESTRATE_API_KEY=${IBM_CLOUD_API_KEY}
ORCHESTRATE_URL=https://orchestrate.watsonx.ibm.com
ORCHESTRATE_WORKSPACE_ID=<workspace_id>

# Natural Language Understanding
NLU_INSTANCE_ID=<watsonx-Hackathon_NLU_id>
NLU_API_KEY=${IBM_CLOUD_API_KEY}
NLU_URL=https://api.us-south.natural-language-understanding.watson.cloud.ibm.com

# Cloudant
CLOUDANT_INSTANCE_ID=<watsonx-Hackathon_Cloudant_id>
CLOUDANT_API_KEY=${IBM_CLOUD_API_KEY}
CLOUDANT_URL=<cloudant_service_url>
CLOUDANT_ACCOUNT=<cloudant_account_name>
CLOUDANT_DATABASE=pipeline_history

# Governance
GOV_INSTANCE_ID=<watsonx-Hackathon_GOV_id>
GOV_API_KEY=${IBM_CLOUD_API_KEY}
GOV_URL=https://api.dataplatform.cloud.ibm.com/v2/governance

# Application Settings
LOG_LEVEL=INFO
MAX_ITERATIONS=3
QUALITY_THRESHOLD=7.0
```

---

## Python Dependencies Update

Add to `requirements.txt`:

```txt
# IBM watsonx
ibm-watsonx-ai>=1.0.0
ibm-cloud-sdk-core>=3.18.0

# IBM Watson Services
ibm-watson>=7.0.0
ibm-watson-openscale>=3.0.0

# Cloudant
cloudant>=2.15.0

# Existing dependencies
fastapi>=0.111.0
httpx>=0.27.0
python-dotenv>=1.0.0
duckduckgo-search>=4.0.0
beautifulsoup4>=4.12.0
detoxify>=0.5.0
```

---

## Service Access Verification

Test each service connection:

```python
# test_services.py
import os
from ibm_watsonx_ai.foundation_models import Model
from ibm_watson import NaturalLanguageUnderstandingV1
from cloudant.client import Cloudant
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

def test_watsonx():
    """Test watsonx.ai connection"""
    try:
        model = Model(
            model_id=os.getenv("WATSONX_MODEL_ID"),
            credentials={"apikey": os.getenv("IBM_CLOUD_API_KEY")},
            project_id=os.getenv("WATSONX_PROJECT_ID")
        )
        result = model.generate_text("Hello")
        print("✓ watsonx.ai: Connected")
        return True
    except Exception as e:
        print(f"✗ watsonx.ai: {str(e)}")
        return False

def test_nlu():
    """Test Watson NLU connection"""
    try:
        nlu = NaturalLanguageUnderstandingV1(
            version='2022-04-07',
            authenticator=IAMAuthenticator(os.getenv('IBM_CLOUD_API_KEY'))
        )
        nlu.set_service_url(os.getenv('NLU_URL'))
        # Simple test
        print("✓ Watson NLU: Connected")
        return True
    except Exception as e:
        print(f"✗ Watson NLU: {str(e)}")
        return False

def test_cloudant():
    """Test Cloudant connection"""
    try:
        client = Cloudant.iam(
            account_name=os.getenv('CLOUDANT_ACCOUNT'),
            api_key=os.getenv('IBM_CLOUD_API_KEY'),
            connect=True
        )
        print("✓ Cloudant: Connected")
        client.disconnect()
        return True
    except Exception as e:
        print(f"✗ Cloudant: {str(e)}")
        return False

if __name__ == "__main__":
    print("Testing IBM Hackathon Services...\n")
    test_watsonx()
    test_nlu()
    test_cloudant()
    print("\nService verification complete!")
```

Run: `python test_services.py`

---

## Quick Start Checklist

- [ ] Get IBM Cloud API key from hackathon organizers
- [ ] Create watsonx.ai project with COS storage
- [ ] Copy PROJECT_ID from project URL
- [ ] Get instance IDs for all services from IBM Cloud dashboard
- [ ] Create `.env` file with all configurations
- [ ] Install Python dependencies: `pip install -r requirements.txt`
- [ ] Run service verification: `python test_services.py`
- [ ] Follow Enhancement 1-A to set up Granite client
- [ ] Proceed with remaining enhancements in order

---

## Support Resources

- **IBM Cloud Dashboard**: https://cloud.ibm.com/
- **watsonx.ai Platform**: https://dataplatform.cloud.ibm.com/
- **IBM Documentation**: https://cloud.ibm.com/docs
- **Hackathon Support**: Contact your hackathon organizers for service-specific issues

---

This configuration leverages ALL your available IBM services for maximum impact and functionality!