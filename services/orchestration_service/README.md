# Orchestration Service

## Overview

The Orchestration Service provides a lightweight agent framework for coordinating multi-agent workflows in the ForgeByBob blog generation system. It implements a pipeline-based architecture where agents can be chained together to perform complex tasks.

## Architecture

### Core Components

1. **Agent Base Class** (`agent_base.py`)
   - Abstract base class for all agents
   - Provides state management and execution tracking
   - Handles error recovery and logging

2. **Agent Registry** (`agent_registry.py`)
   - Manages agent class registration
   - Creates and tracks agent instances
   - Provides agent discovery

3. **Pipeline Manager** (`pipeline_manager.py`)
   - Orchestrates multi-agent workflows
   - Manages data flow between agents
   - Tracks pipeline execution state

4. **Agents** (`agents/`)
   - **WriterAgent**: Generates blog content using IBM Granite
   - **PublisherAgent**: Saves generated content to storage

## API Endpoints

### Health Check
```
GET /health
```
Returns service health status.

### List Agents
```
GET /agents
```
Returns all registered agent classes and instances.

### Create Pipeline
```
POST /pipelines
{
  "name": "My Pipeline",
  "steps": [
    {
      "agent_name": "writer",
      "input_mapping": {...}
    }
  ]
}
```

### List Pipelines
```
GET /pipelines
```
Returns all created pipelines and their status.

### Get Pipeline Status
```
GET /pipelines/{pipeline_id}
```
Returns detailed status of a specific pipeline.

### Execute Pipeline
```
POST /pipelines/{pipeline_id}/execute
{
  "pipeline_id": "...",
  "input_data": {...}
}
```

### Generate Blog (Convenience Endpoint)
```
POST /blog/generate
{
  "prompt": "Write a blog about...",
  "blog_id": "optional-id",
  "tone": "professional"
}
```
Creates and executes a Writer → Publisher pipeline.

## Usage Examples

### Direct API Usage

```python
import httpx
import asyncio

async def generate_blog():
    async with httpx.AsyncClient() as client:
        response = await client.post(
            "http://localhost:8004/blog/generate",
            json={
                "prompt": "Write about AI in healthcare",
                "tone": "professional"
            },
            timeout=60.0
        )
        return response.json()

result = asyncio.run(generate_blog())
print(result)
```

### Via API Gateway

```python
import httpx
import asyncio

async def generate_via_gateway():
    async with httpx.AsyncClient() as client:
        response = await client.post(
            "http://localhost:8000/api/blogs/generate-orchestrated",
            json={
                "prompt": "Write about cloud computing",
                "tone": "casual"
            },
            timeout=60.0
        )
        return response.json()

result = asyncio.run(generate_via_gateway())
print(result)
```

### Via Web UI

1. Navigate to http://localhost:8003/create
2. Fill in the blog details
3. Check "Use Agent Orchestration"
4. Submit the form

## Adding New Agents

### Step 1: Create Agent Class

```python
# services/orchestration_service/agents/my_agent.py
from ..agent_base import BaseAgent, AgentResult
from typing import Dict, Any

class MyAgent(BaseAgent):
    """My custom agent"""
    
    async def execute(self, input_data: Dict[str, Any]) -> AgentResult:
        try:
            # Your agent logic here
            result_data = {"output": "processed data"}
            
            return AgentResult(
                success=True,
                data=result_data,
                metadata={"agent": "my_agent"}
            )
        except Exception as e:
            return AgentResult(
                success=False,
                error=str(e)
            )
```

### Step 2: Register Agent

```python
# services/orchestration_service/agents/__init__.py
from .my_agent import MyAgent

__all__ = ['WriterAgent', 'PublisherAgent', 'MyAgent']
```

### Step 3: Register in Main Service

```python
# services/orchestration_service/main.py
from .agents import WriterAgent, PublisherAgent, MyAgent

@app.on_event("startup")
async def startup_event():
    agent_registry.register_agent_class("writer", WriterAgent)
    agent_registry.register_agent_class("publisher", PublisherAgent)
    agent_registry.register_agent_class("my_agent", MyAgent)
```

## Configuration

The service runs on port **8004** by default.

To change the port, modify the `main.py` file:

```python
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8004)
```

## Testing

Run the test suite:

```bash
python test_orchestration.py
```

This will test:
- Service health
- Agent registration
- Blog generation pipeline
- API Gateway integration
- Pipeline listing

## Monitoring

### Agent Status

Check agent status:
```bash
curl http://localhost:8004/agents
```

### Pipeline Status

Check pipeline status:
```bash
curl http://localhost:8004/pipelines
```

### Logs

The service logs all agent executions and pipeline operations. Check the console output for detailed information.

## Future Enhancements

The current implementation provides a foundation for:

1. **Research Agent** - Web search and content research
2. **Reviewer Agent** - Content quality review and suggestions
3. **SEO Agent** - SEO optimization and keyword analysis
4. **Image Agent** - Image generation and selection
5. **Fact-Checker Agent** - Verify claims and citations

These agents can be added incrementally without disrupting the existing system.

## Troubleshooting

### Service Won't Start

1. Check if port 8004 is available
2. Verify all dependencies are installed
3. Check that watsonx service is running

### Agent Execution Fails

1. Check agent logs for error details
2. Verify input data format
3. Ensure IBM credentials are configured

### Pipeline Hangs

1. Check timeout settings (default 60s)
2. Verify all agents in pipeline are registered
3. Check for circular dependencies

## Support

For issues or questions, refer to:
- Main project README
- Enhancement documentation
- IBM watsonx.ai documentation