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
    
    @property
    def pipelines(self) -> Dict[str, Pipeline]:
        """Get all pipelines"""
        return self._pipelines
    
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
    
    def get_metrics(self) -> Dict[str, Any]:
        """Get aggregated metrics across all pipelines"""
        total_pipelines = len(self.pipelines)
        completed = sum(1 for p in self.pipelines.values() if p.state == "completed")
        failed = sum(1 for p in self.pipelines.values() if p.state == "failed")
        running = sum(1 for p in self.pipelines.values() if p.state == "running")
        
        # Calculate average duration for completed pipelines
        durations = []
        for pipeline in self.pipelines.values():
            if pipeline.state == "completed" and pipeline.start_time and pipeline.end_time:
                duration = (pipeline.end_time - pipeline.start_time).total_seconds()
                durations.append(duration)
        
        avg_duration = sum(durations) / len(durations) if durations else 0
        
        # Agent usage statistics
        agent_usage = {}
        for pipeline in self.pipelines.values():
            for step in pipeline.steps:
                agent_name = step.agent_name
                if agent_name not in agent_usage:
                    agent_usage[agent_name] = {"total": 0, "success": 0, "failed": 0}
                
                agent_usage[agent_name]["total"] += 1
                if step.result:
                    if step.result.success:
                        agent_usage[agent_name]["success"] += 1
                    else:
                        agent_usage[agent_name]["failed"] += 1
        
        return {
            "total_pipelines": total_pipelines,
            "completed": completed,
            "failed": failed,
            "running": running,
            "success_rate": (completed / total_pipelines * 100) if total_pipelines > 0 else 0,
            "avg_duration_seconds": round(avg_duration, 2),
            "agent_usage": agent_usage
        }


# Global pipeline manager instance
pipeline_manager = PipelineManager()

# Made with Bob
