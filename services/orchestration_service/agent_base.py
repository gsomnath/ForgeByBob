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
    
    # Agent metadata - override in subclasses
    display_name: str = "Base Agent"
    description: str = "Base agent class"
    input_schema: Dict[str, str] = {}
    output_schema: Dict[str, str] = {}
    
    def __init__(self, agent_id: Optional[str] = None):
        self.agent_id = agent_id or str(uuid.uuid4())
        self.agent_name = self.__class__.__name__
        self.state = AgentState.IDLE
        self.execution_history = []
        logger.info(f"Agent initialized: {self.agent_name} ({self.agent_id})")
    
    @classmethod
    def get_metadata(cls) -> Dict[str, Any]:
        """Get agent metadata"""
        return {
            "name": cls.__name__,
            "display_name": cls.display_name,
            "description": cls.description,
            "input_schema": cls.input_schema,
            "output_schema": cls.output_schema
        }
    
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

# Made with Bob
