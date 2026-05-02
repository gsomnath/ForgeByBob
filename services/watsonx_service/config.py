"""
Configuration for IBM watsonx.ai Granite client
"""
from pydantic import BaseModel
from typing import Optional
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class GraniteConfig(BaseModel):
    """Configuration for Granite LLM"""
    
    # IBM Cloud credentials
    api_key: str
    project_id: str
    url: str = "https://us-south.ml.cloud.ibm.com"
    
    # Model configuration
    model_id: str = "ibm/granite-4-h-small"
    
    # Generation parameters
    max_new_tokens: int = 2048
    temperature: float = 0.7
    top_p: float = 0.9
    top_k: int = 50
    repetition_penalty: float = 1.1
    
    @classmethod
    def from_env(cls) -> "GraniteConfig":
        """Load configuration from environment variables"""
        return cls(
            api_key=os.getenv("IBM_CLOUD_API_KEY", ""),
            project_id=os.getenv("WATSONX_PROJECT_ID", ""),
            url=os.getenv("WATSONX_URL", "https://us-south.ml.cloud.ibm.com"),
            model_id=os.getenv("WATSONX_MODEL_ID", "ibm/granite-3-8b-instruct")
        )
    
    def validate_credentials(self) -> bool:
        """Validate that required credentials are present"""
        return bool(self.api_key and self.project_id)


# Global config instance
granite_config = GraniteConfig.from_env()

# Made with Bob
