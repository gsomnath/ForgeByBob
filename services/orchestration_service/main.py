"""
Orchestration Service - Manages agent pipelines
"""
from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
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

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:8003",  # UI Service
        "http://127.0.0.1:8003",
        "http://localhost:8000",  # API Gateway
        "http://127.0.0.1:8000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
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
            "agent_instances": agent_registry.list_agents(),
            "agent_metadata": agent_registry.get_agent_metadata()
        }
    }


@app.post("/agents/{agent_name}/run")
async def run_agent(agent_name: str, input_data: Dict[str, Any]):
    """
    Run a single agent with provided input
    
    Args:
        agent_name: Name of the agent to run (e.g., "writer", "publisher")
        input_data: Input data for the agent
    
    Returns:
        Agent execution result
    """
    try:
        # Create agent instance
        agent = agent_registry.create_agent(agent_name)
        
        # Run agent
        result = await agent.run(input_data)
        
        return {
            "success": True,
            "message": f"{agent_name} agent executed successfully",
            "data": result.to_dict()
        }
        
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        logger.error(f"Failed to run agent {agent_name}: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/metrics")
async def get_metrics():
    """Get orchestration metrics"""
    return {
        "success": True,
        "data": pipeline_manager.get_metrics()
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

# Made with Bob
