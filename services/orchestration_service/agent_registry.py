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
    
    def get_agent_metadata(self) -> Dict[str, Dict]:
        """Get metadata for all registered agent classes"""
        metadata = {}
        for name, agent_class in self._agent_classes.items():
            metadata[name] = agent_class.get_metadata()
        return metadata


# Global registry instance
agent_registry = AgentRegistry()

# Made with Bob
