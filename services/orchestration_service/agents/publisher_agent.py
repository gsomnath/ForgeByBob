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
    
    # Agent metadata
    display_name = "Publisher Agent"
    description = "Saves and publishes blog content to storage. Creates structured blog records with metadata and timestamps for easy retrieval and management."
    input_schema = {
        "content": "Blog content to publish (required)",
        "blog_id": "Optional blog ID (auto-generated if not provided)",
        "metadata": "Optional metadata dictionary"
    }
    output_schema = {
        "blog_id": "Published blog ID",
        "file_path": "Storage file path",
        "published_at": "Publication timestamp",
        "word_count": "Content word count"
    }
    
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

# Made with Bob
