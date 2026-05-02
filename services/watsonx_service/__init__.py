"""
IBM watsonx.ai Service
Provides Granite LLM client for blog content generation
"""
from .granite_client import GraniteClient, get_granite_client
from .config import GraniteConfig, granite_config

__all__ = ['GraniteClient', 'get_granite_client', 'GraniteConfig', 'granite_config']

# Made with Bob
