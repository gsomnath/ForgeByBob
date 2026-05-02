# Enhancement 1-B: IBM watsonx Orchestrate Setup & Agent Framework

## Module Overview
This module sets up IBM watsonx Orchestrate and creates the foundational agent framework. This is **fully functional** and enables basic agent coordination without requiring all 5 agents to be implemented.

## What This Module Delivers
- ✅ IBM watsonx Orchestrate workspace configured
- ✅ Agent framework and base classes created
- ✅ Simple 2-agent pipeline working (Writer → Publisher)
- ✅ Real-time agent status tracking
- ✅ Foundation for adding more agents incrementally

## Prerequisites
- Enhancement 1-A completed (Granite client working)
- IBM Cloud account with watsonx.ai access
- Python 3.11+

## Implementation Time: 2-3 hours

---

## Part 1: IBM watsonx Orchestrate Setup (45 minutes)

### Step 1.1: Access watsonx Orchestrate

**Action Steps:**
1. Log into IBM Cloud: https://cloud.ibm.com/
2. Navigate to "Catalog"
3. Search for "watsonx Orchestrate"
4. Click on "watsonx Orchestrate"

**Note:** As of 2024, watsonx Orchestrate may require:
- Enterprise account OR
- Trial access request

**Alternative for Hackathon:**
If Orchestrate is not immediately available, we'll implement a **lightweight orchestration layer** that demonstrates the same concepts and can be upgraded to full Orchestrate later.

### Step 1.2: Request Trial Access (if needed)

**Action Steps:**
1. Go to: https://www.ibm.com/products/watsonx-orchestrate
2. Click "Request a demo" or "Start free trial"
3. Fill in form:
   ```
   Name: [Your name]
   Email: [Your email]
   Company: [Your company/university]
   Use case: AI-powered blog generation with autonomous agents
   ```
4. Wait for approval email (usually 1-2 business days)

**For Hackathon Timeline:**
We'll proceed with the lightweight orchestration layer that can be upgraded to full Orchestrate when access is granted.

---

## Part 2: Lightweight Orchestration Layer (1 hour)

### Step 2.1: Create Orchestration Service Structure

**Action Steps:**
```bash
# Create orchestration service directory
mkdir -p services/orchestration_service
cd services/orchestration_service

# Create files
touch __init__.py
touch agent_base.py
touch agent_registry.py
touch pipeline_manager.py
touch main.py
```

### Step 2.2: Implement Agent Base Class

**File: `services/orchestration_service/agent_base.py`**

```python
"""
Base class for all agents in the system
"""
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
from enum import Enum
import logging
from datetime import datetime
import uuid

logger = logging.getLogger(__name__)


class AgentState(Enum):
    """Agent execution states"""
    IDLE = "idle"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    WAITING = "waiting"


class AgentResult:
    """Result from agent execution"""
    
    def __init__(
        self,
        success: bool,
        data: Any = None,
        error: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None
    ):
        self.success = success
        self.data = data
        self.error = error
        self.metadata = metadata or {}
        self.timestamp = datetime.utcnow().isoformat()
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            "success": self.success,
            "data": self.data,
            "error": self.error,
            "metadata": self.metadata,
            "timestamp": self.timestamp
        }


class BaseAgent(ABC):
    """Base class for all agents"""
    
    def __init__(self, agent_id: Optional[str] = None):
        self.agent_id = agent_id or str(uuid.uuid4())
        self.agent_name = self.__class__.__name__
        self.state = AgentState.IDLE
        self.execution_history = []
        logger.info(f"Agent initialized: {self.agent_name} ({self.agent_id})")
    
    @abstractmethod
    async def execute(self, input_data: Dict[str, Any]) -> AgentResult:
        """
        Execute the agent's main task
        
        Args:
            input_data: Input data for the agent
            
        Returns:
            AgentResult with success status and output data
        """
        pass
    
    async def run(self, input_data: Dict[str, Any]) -> AgentResult:
        """
        Run the agent with state management
        
        Args:
            input_data: Input data for the agent
            
        Returns:
            AgentResult
        """
        execution_id = str(uuid.uuid4())
        start_time = datetime.utcnow()
        
        try:
            logger.info(f"{self.agent_name}: Starting execution {execution_id}")
            self.state = AgentState.RUNNING
            
            # Execute agent logic
            result = await self.execute(input_data)
            
            # Update state
            self.state = AgentState.COMPLETED if result.success else AgentState.FAILED
            
            # Record execution
            execution_record = {
                "execution_id": execution_id,
                "start_time": start_time.isoformat(),
                "end_time": datetime.utcnow().isoformat(),
                "duration_seconds": (datetime.utcnow() - start_time).total_seconds(),
                "state": self.state.value,
                "result": result.to_dict()
            }
            self.execution_history.append(execution_record)
            
            logger.info(
                f"{self.agent_name}: Execution {execution_id} "
                f"{'succeeded' if result.success else 'failed'}"
            )
            
            return result
            
        except Exception as e:
            logger.error(f"{self.agent_name}: Execution {execution_id} failed: {str(e)}")
            self.state = AgentState.FAILED
            
            error_result = AgentResult(
                success=False,
                error=str(e),
                metadata={"execution_id": execution_id}
            )
            
            execution_record = {
                "execution_id": execution_id,
                "start_time": start_time.isoformat(),
                "end_time": datetime.utcnow().isoformat(),
                "duration_seconds": (datetime.utcnow() - start_time).total_seconds(),
                "state": self.state.value,
                "result": error_result.to_dict()
            }
            self.execution_history.append(execution_record)
            
            return error_result
    
    def get_status(self) -> Dict[str, Any]:
        """Get current agent status"""
        return {
            "agent_id": self.agent_id,
            "agent_name": self.agent_name,
            "state": self.state.value,
            "execution_count": len(self.execution_history),
            "last_execution": self.execution_history[-1] if self.execution_history else None
        }
    
    def reset(self):
        """Reset agent state"""
        self.state = AgentState.IDLE
        logger.info(f"{self.agent_name}: State reset to IDLE")
```

### Step 2.3: Implement Agent Registry

**File: `services/orchestration_service/agent_registry.py`**

```python
"""
Registry for managing agents
"""
from typing import Dict, Type, Optional
from .agent_base import BaseAgent
import logging

logger = logging.getLogger(__name__)


class AgentRegistry:
    """Registry for managing agent instances"""
    
    def __init__(self):
        self._agents: Dict[str, BaseAgent] = {}
        self._agent_classes: Dict[str, Type[BaseAgent]] = {}
        logger.info("Agent registry initialized")
    
    def register_agent_class(self, name: str, agent_class: Type[BaseAgent]):
        """
        Register an agent class
        
        Args:
            name: Agent name (e.g., "writer", "reviewer")
            agent_class: Agent class (subclass of BaseAgent)
        """
        self._agent_classes[name] = agent_class
        logger.info(f"Registered agent class: {name}")
    
    def create_agent(self, name: str, agent_id: Optional[str] = None) -> BaseAgent:
        """
        Create an agent instance
        
        Args:
            name: Agent name
            agent_id: Optional agent ID
            
        Returns:
            Agent instance
        """
        if name not in self._agent_classes:
            raise ValueError(f"Agent class not registered: {name}")
        
        agent_class = self._agent_classes[name]
        agent = agent_class(agent_id=agent_id)
        
        self._agents[agent.agent_id] = agent
        logger.info(f"Created agent: {name} ({agent.agent_id})")
        
        return agent
    
    def get_agent(self, agent_id: str) -> Optional[BaseAgent]:
        """Get agent by ID"""
        return self._agents.get(agent_id)
    
    def list_agents(self) -> Dict[str, Dict]:
        """List all agents and their status"""
        return {
            agent_id: agent.get_status()
            for agent_id, agent in self._agents.items()
        }
    
    def list_agent_classes(self) -> list:
        """List registered agent classes"""
        return list(self._agent_classes.keys())


# Global registry instance
agent_registry = AgentRegistry()
```

### Step 2.4: Implement Pipeline Manager

**File: `services/orchestration_service/pipeline_manager.py`**

```python
"""
Pipeline manager for orchestrating agent workflows
"""
from typing import List, Dict, Any, Optional
from .agent_base import BaseAgent, AgentResult, AgentState
from .agent_registry import agent_registry
import logging
import uuid
from datetime import datetime
import asyncio

logger = logging.getLogger(__name__)


class PipelineStep:
    """Single step in a pipeline"""
    
    def __init__(
        self,
        agent_name: str,
        input_mapping: Optional[Dict[str, str]] = None,
        condition: Optional[str] = None
    ):
        self.agent_name = agent_name
        self.input_mapping = input_mapping or {}
        self.condition = condition  # For conditional execution
        self.agent_id: Optional[str] = None
        self.result: Optional[AgentResult] = None


class Pipeline:
    """Agent execution pipeline"""
    
    def __init__(self, pipeline_id: Optional[str] = None, name: str = "Unnamed Pipeline"):
        self.pipeline_id = pipeline_id or str(uuid.uuid4())
        self.name = name
        self.steps: List[PipelineStep] = []
        self.state = "idle"
        self.current_step = 0
        self.context: Dict[str, Any] = {}
        self.start_time: Optional[datetime] = None
        self.end_time: Optional[datetime] = None
        logger.info(f"Pipeline created: {name} ({self.pipeline_id})")
    
    def add_step(
        self,
        agent_name: str,
        input_mapping: Optional[Dict[str, str]] = None,
        condition: Optional[str] = None
    ):
        """Add a step to the pipeline"""
        step = PipelineStep(agent_name, input_mapping, condition)
        self.steps.append(step)
        logger.info(f"Added step to pipeline {self.name}: {agent_name}")
    
    async def execute(self, initial_input: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute the pipeline
        
        Args:
            initial_input: Initial input data
            
        Returns:
            Pipeline execution result
        """
        self.state = "running"
        self.start_time = datetime.utcnow()
        self.context = {"initial_input": initial_input}
        
        logger.info(f"Starting pipeline execution: {self.name}")
        
        try:
            for i, step in enumerate(self.steps):
                self.current_step = i
                logger.info(f"Pipeline {self.name}: Executing step {i+1}/{len(self.steps)} - {step.agent_name}")
                
                # Create agent instance
                agent = agent_registry.create_agent(step.agent_name)
                step.agent_id = agent.agent_id
                
                # Prepare input data
                if i == 0:
                    # First step uses initial input
                    input_data = initial_input
                else:
                    # Subsequent steps use previous step's output
                    prev_result = self.steps[i-1].result
                    if prev_result and prev_result.success:
                        input_data = prev_result.data
                    else:
                        raise Exception(f"Previous step failed: {step.agent_name}")
                
                # Apply input mapping if specified
                if step.input_mapping:
                    mapped_input = {}
                    for target_key, source_key in step.input_mapping.items():
                        if source_key in input_data:
                            mapped_input[target_key] = input_data[source_key]
                    input_data = mapped_input
                
                # Execute agent
                result = await agent.run(input_data)
                step.result = result
                
                # Store result in context
                self.context[f"step_{i}_{step.agent_name}"] = result.to_dict()
                
                # Check if step failed
                if not result.success:
                    logger.error(f"Pipeline {self.name}: Step {i+1} failed - {step.agent_name}")
                    self.state = "failed"
                    break
                
                logger.info(f"Pipeline {self.name}: Step {i+1} completed successfully")
            
            # Pipeline completed
            if self.state != "failed":
                self.state = "completed"
                logger.info(f"Pipeline {self.name}: Execution completed successfully")
            
        except Exception as e:
            logger.error(f"Pipeline {self.name}: Execution failed: {str(e)}")
            self.state = "failed"
            self.context["error"] = str(e)
        
        finally:
            self.end_time = datetime.utcnow()
            duration = (self.end_time - self.start_time).total_seconds()
            self.context["duration_seconds"] = duration
        
        return self.get_status()
    
    def get_status(self) -> Dict[str, Any]:
        """Get pipeline status"""
        return {
            "pipeline_id": self.pipeline_id,
            "name": self.name,
            "state": self.state,
            "current_step": self.current_step,
            "total_steps": len(self.steps),
            "steps": [
                {
                    "agent_name": step.agent_name,
                    "agent_id": step.agent_id,
                    "completed": step.result is not None,
                    "success": step.result.success if step.result else None
                }
                for step in self.steps
            ],
            "start_time": self.start_time.isoformat() if self.start_time else None,
            "end_time": self.end_time.isoformat() if self.end_time else None,
            "duration_seconds": self.context.get("duration_seconds")
        }


class PipelineManager:
    """Manager for creating and executing pipelines"""
    
    def __init__(self):
        self._pipelines: Dict[str, Pipeline] = {}
        logger.info("Pipeline manager initialized")
    
    def create_pipeline(self, name: str) -> Pipeline:
        """Create a new pipeline"""
        pipeline = Pipeline(name=name)
        self._pipelines[pipeline.pipeline_id] = pipeline
        return pipeline
    
    def get_pipeline(self, pipeline_id: str) -> Optional[Pipeline]:
        """Get pipeline by ID"""
        return self._pipelines.get(pipeline_id)
    
    def list_pipelines(self) -> Dict[str, Dict]:
        """List all pipelines"""
        return {
            pipeline_id: pipeline.get_status()
            for pipeline_id, pipeline in self._pipelines.items()
        }
    
    async def execute_pipeline(
        self,
        pipeline_id: str,
        initial_input: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Execute a pipeline"""
        pipeline = self.get_pipeline(pipeline_id)
        if not pipeline:
            raise ValueError(f"Pipeline not found: {pipeline_id}")
        
        return await pipeline.execute(initial_input)


# Global pipeline manager instance
pipeline_manager = PipelineManager()
```

### Step 2.5: Create Simple Writer Agent

**File: `services/orchestration_service/agents/writer_agent.py`**

```bash
# Create agents directory
mkdir -p services/orchestration_service/agents
touch services/orchestration_service/agents/__init__.py
```

```python
"""
Writer Agent - Generates blog content using Granite
"""
from ..agent_base import BaseAgent, AgentResult
from services.watsonx_service.granite_client import get_granite_client
from typing import Dict, Any
import logging

logger = logging.getLogger(__name__)


class WriterAgent(BaseAgent):
    """Agent for generating blog content"""
    
    def __init__(self, agent_id=None):
        super().__init__(agent_id)
        self.granite = get_granite_client()
        self.system_prompt = """You are a professional blog writer with expertise in 
        creating engaging, well-structured content. Write in a clear, accessible style 
        with proper formatting, headings, and SEO optimization. Always include:
        - Compelling title
        - Engaging introduction
        - Well-structured body with headings
        - Strong conclusion with call-to-action
        """
    
    async def execute(self, input_data: Dict[str, Any]) -> AgentResult:
        """
        Generate blog content
        
        Expected input_data:
        {
            "prompt": "Blog topic or instructions",
            "research_brief": "Optional research context",
            "tone": "Optional tone specification"
        }
        
        Returns:
            AgentResult with generated content
        """
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
            
            return AgentResult(
                success=True,
                data={
                    "content": content,
                    "word_count": len(content.split()),
                    "char_count": len(content),
                    "model": "ibm/granite-3-8b-instruct"
                },
                metadata={
                    "prompt": prompt,
                    "tone": tone
                }
            )
            
        except Exception as e:
            logger.error(f"WriterAgent: Failed to generate content: {str(e)}")
            return AgentResult(
                success=False,
                error=str(e)
            )
```

### Step 2.6: Create Simple Publisher Agent

**File: `services/orchestration_service/agents/publisher_agent.py`**

```python
"""
Publisher Agent - Saves blog content to storage
"""
from ..agent_base import BaseAgent, AgentResult
from typing import Dict, Any
import logging
import json
from pathlib import Path
from datetime import datetime

logger = logging.getLogger(__name__)


class PublisherAgent(BaseAgent):
    """Agent for publishing blog content"""
    
    def __init__(self, agent_id=None):
        super().__init__(agent_id)
        self.storage_path = Path("data/published_blogs")
        self.storage_path.mkdir(parents=True, exist_ok=True)
    
    async def execute(self, input_data: Dict[str, Any]) -> AgentResult:
        """
        Publish blog content
        
        Expected input_data:
        {
            "content": "Blog content to publish",
            "blog_id": "Optional blog ID",
            "metadata": "Optional metadata"
        }
        
        Returns:
            AgentResult with publication details
        """
        try:
            content = input_data.get("content", "")
            blog_id = input_data.get("blog_id", f"blog_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}")
            metadata = input_data.get("metadata", {})
            
            if not content:
                return AgentResult(
                    success=False,
                    error="No content provided"
                )
            
            # Create blog record
            blog_record = {
                "blog_id": blog_id,
                "content": content,
                "published_at": datetime.utcnow().isoformat(),
                "word_count": len(content.split()),
                "metadata": metadata
            }
            
            # Save to file
            file_path = self.storage_path / f"{blog_id}.json"
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(blog_record, f, indent=2, ensure_ascii=False)
            
            logger.info(f"PublisherAgent: Published blog {blog_id} to {file_path}")
            
            return AgentResult(
                success=True,
                data={
                    "blog_id": blog_id,
                    "file_path": str(file_path),
                    "published_at": blog_record["published_at"],
                    "word_count": blog_record["word_count"]
                },
                metadata={
                    "storage_path": str(self.storage_path)
                }
            )
            
        except Exception as e:
            logger.error(f"PublisherAgent: Failed to publish: {str(e)}")
            return AgentResult(
                success=False,
                error=str(e)
            )
```

### Step 2.7: Register Agents

**File: `services/orchestration_service/agents/__init__.py`**

```python
"""
Agent implementations
"""
from .writer_agent import WriterAgent
from .publisher_agent import PublisherAgent

__all__ = ['WriterAgent', 'PublisherAgent']
```

### Step 2.8: Create Orchestration Service API

**File: `services/orchestration_service/main.py`**

```python
"""
Orchestration Service - Manages agent pipelines
"""
from fastapi import FastAPI, HTTPException, BackgroundTasks
from pydantic import BaseModel
from typing import Dict, Any, Optional
import logging

from .agent_registry import agent_registry
from .pipeline_manager import pipeline_manager
from .agents import WriterAgent, PublisherAgent

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Orchestration Service",
    description="Agent orchestration and pipeline management",
    version="1.0.0"
)


# Request models
class PipelineRequest(BaseModel):
    name: str
    steps: list[Dict[str, Any]]


class ExecutionRequest(BaseModel):
    pipeline_id: str
    input_data: Dict[str, Any]


class BlogGenerationRequest(BaseModel):
    prompt: str
    blog_id: Optional[str] = None
    tone: Optional[str] = "professional"


# Initialize agents
@app.on_event("startup")
async def startup_event():
    """Register agents on startup"""
    logger.info("Registering agents...")
    agent_registry.register_agent_class("writer", WriterAgent)
    agent_registry.register_agent_class("publisher", PublisherAgent)
    logger.info("Agents registered successfully")


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "service": "Orchestration Service",
        "version": "1.0.0",
        "status": "active"
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}


@app.get("/agents")
async def list_agents():
    """List all registered agents"""
    return {
        "success": True,
        "data": {
            "agent_classes": agent_registry.list_agent_classes(),
            "agent_instances": agent_registry.list_agents()
        }
    }


@app.post("/pipelines")
async def create_pipeline(request: PipelineRequest):
    """Create a new pipeline"""
    try:
        pipeline = pipeline_manager.create_pipeline(request.name)
        
        for step in request.steps:
            pipeline.add_step(
                agent_name=step["agent_name"],
                input_mapping=step.get("input_mapping"),
                condition=step.get("condition")
            )
        
        return {
            "success": True,
            "data": {
                "pipeline_id": pipeline.pipeline_id,
                "name": pipeline.name,
                "steps": len(pipeline.steps)
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/pipelines")
async def list_pipelines():
    """List all pipelines"""
    return {
        "success": True,
        "data": pipeline_manager.list_pipelines()
    }


@app.get("/pipelines/{pipeline_id}")
async def get_pipeline_status(pipeline_id: str):
    """Get pipeline status"""
    pipeline = pipeline_manager.get_pipeline(pipeline_id)
    if not pipeline:
        raise HTTPException(status_code=404, detail="Pipeline not found")
    
    return {
        "success": True,
        "data": pipeline.get_status()
    }


@app.post("/pipelines/{pipeline_id}/execute")
async def execute_pipeline(pipeline_id: str, request: ExecutionRequest):
    """Execute a pipeline"""
    try:
        result = await pipeline_manager.execute_pipeline(
            pipeline_id=request.pipeline_id,
            initial_input=request.input_data
        )
        
        return {
            "success": True,
            "data": result
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/blog/generate")
async def generate_blog(request: BlogGenerationRequest):
    """
    Generate blog using Writer → Publisher pipeline
    
    This is a convenience endpoint that creates and executes
    a simple 2-agent pipeline.
    """
    try:
        # Create pipeline
        pipeline = pipeline_manager.create_pipeline("Blog Generation Pipeline")
        pipeline.add_step("writer")
        pipeline.add_step("publisher")
        
        # Execute pipeline
        input_data = {
            "prompt": request.prompt,
            "blog_id": request.blog_id,
            "tone": request.tone
        }
        
        result = await pipeline.execute(input_data)
        
        return {
            "success": True,
            "message": "Blog generated successfully",
            "data": result
        }
        
    except Exception as e:
        logger.error(f"Blog generation failed: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8004)
```

---

## Part 3: Testing the Orchestration Layer (30 minutes)

### Step 3.1: Start Orchestration Service

```bash
# Terminal 1: Start orchestration service
python -m services.orchestration_service.main
```

**Expected Output:**
```
INFO:     Started server process
INFO:     Waiting for application startup.
INFO:     Registering agents...
INFO:     Agents registered successfully
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8004
```

### Step 3.2: Test Agent Registration

```bash
# Terminal 2: Test agents endpoint
curl http://localhost:8004/agents
```

**Expected Response:**
```json
{
  "success": true,
  "data": {
    "agent_classes": ["writer", "publisher"],
    "agent_instances": {}
  }
}
```

### Step 3.3: Test Blog Generation

```bash
# Test blog generation
curl -X POST http://localhost:8004/blog/generate \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "Write about the benefits of AI in healthcare",
    "tone": "professional"
  }'
```

**Expected Response:**
```json
{
  "success": true,
  "message": "Blog generated successfully",
  "data": {
    "pipeline_id": "...",
    "state": "completed",
    "steps": [
      {
        "agent_name": "writer",
        "completed": true,
        "success": true
      },
      {
        "agent_name": "publisher",
        "completed": true,
        "success": true
      }
    ]
  }
}
```

### Step 3.4: Verify Published Blog

```bash
# Check published blogs directory
ls data/published_blogs/

# View published blog
cat data/published_blogs/blog_*.json
```

---

## Part 4: Integration with Existing Services (30 minutes)

### Step 4.1: Update API Gateway

**File: `services/api_gateway/main.py`**

Add orchestration service routes:

```python
# Add to imports
ORCHESTRATION_SERVICE_URL = "http://localhost:8004"

# Add new endpoint
@app.post("/api/blogs/generate-orchestrated")
async def generate_blog_orchestrated(request: dict):
    """Generate blog using orchestration service"""
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{ORCHESTRATION_SERVICE_URL}/blog/generate",
                json=request,
                timeout=60.0
            )
            return response.json()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/orchestration/pipelines")
async def list_pipelines():
    """List all orchestration pipelines"""
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{ORCHESTRATION_SERVICE_URL}/pipelines")
            return response.json()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
```

### Step 4.2: Update UI Service

**File: `services/ui_service/templates/create.html`**

Add orchestration option:

```html
<form method="post" action="/create">
    <!-- Existing fields -->
    
    <div class="form-group">
        <label>
            <input type="checkbox" name="use_orchestration" value="true">
            Use Agent Orchestration (Writer → Publisher)
        </label>
    </div>
    
    <button type="submit">Create Blog</button>
</form>
```

---

## Success Criteria

### ✅ Module Complete When:
1. Orchestration service starts successfully
2. Agents are registered and listed
3. Simple 2-agent pipeline executes successfully
4. Blog is generated and published
5. Pipeline status can be queried
6. Integration with existing services works

### 📊 Metrics:
- **Pipeline execution time**: 10-15 seconds
- **Success rate**: >95%
- **Agent coordination**: Working correctly

---

## Next Steps

After completing this module, you can add more agents:
- **Enhancement 1-C**: Research Agent
- **Enhancement 1-D**: Reviewer Agent with Self-Correction
- **Enhancement 1-E**: Real-time Dashboard

This modular approach allows incremental development and testing.