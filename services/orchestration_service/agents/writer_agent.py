"""
Writer Agent - Generates blog content using Granite
"""
from ..agent_base import BaseAgent, AgentResult
from services.watsonx_service.granite_client import get_granite_client
from typing import Dict, Any
import logging
import httpx
from datetime import datetime

logger = logging.getLogger(__name__)

# Service URLs
BLOG_SERVICE_URL = "http://localhost:8001"


class WriterAgent(BaseAgent):
    """Agent for generating blog content"""
    
    # Agent metadata
    display_name = "Writer Agent"
    description = "Generates high-quality blog content using IBM Granite AI. Creates engaging, well-structured articles with proper formatting, headings, and SEO optimization."
    input_schema = {
        "prompt": "Blog topic or instructions (required)",
        "research_brief": "Optional research context",
        "tone": "Writing tone (default: professional)"
    }
    output_schema = {
        "content": "Generated blog content",
        "word_count": "Number of words",
        "char_count": "Number of characters",
        "model": "AI model used"
    }
    
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
        Generate blog content and save as draft
        
        Expected input_data:
        {
            "prompt": "Blog topic or instructions",
            "research_brief": "Optional research context",
            "tone": "Optional tone specification"
        }
        
        Returns:
            AgentResult with generated content and blog draft info
        """
        start_time = datetime.utcnow()
        
        try:
            prompt = input_data.get("prompt", "")
            research_brief = input_data.get("research_brief", "")
            tone = input_data.get("tone", "professional")
            
            if not prompt:
                return AgentResult(
                    success=False,
                    error="No prompt provided"
                )
            
            logger.info(f"WriterAgent: Generating content for prompt: {prompt[:50]}...")
            
            # Extract title from prompt for blog creation
            title_parts = prompt.split('\n')[0].strip()
            title = title_parts[:100] if title_parts else "AI Generated Blog"
            
            # Create draft blog via blog service FIRST
            blog_id = None
            blog_created = False
            
            try:
                async with httpx.AsyncClient(timeout=60.0) as client:
                    # Create blog draft
                    blog_data = {
                        "title": title,
                        "description": f"Generated from prompt: {prompt[:100]}",
                        "tags": ["ai-generated", "draft"],
                        "publication_site": None,  # Let it default to None instead of invalid value
                        "initial_prompt": prompt
                    }
                    
                    logger.info(f"WriterAgent: Creating draft blog via API...")
                    create_response = await client.post(
                        f"{BLOG_SERVICE_URL}/blogs",
                        json=blog_data
                    )
                    
                    if create_response.status_code == 200:
                        create_result = create_response.json()
                        if create_result.get("success"):
                            blog_id = create_result["data"]["id"]
                            blog_created = True
                            logger.info(f"WriterAgent: Created draft blog {blog_id}")
                            
                            # Now generate content using blog service's generate endpoint
                            # This will properly log the API call to WatsonX logs
                            generate_data = {
                                "prompt": prompt,
                                "generation_type": "text"
                            }
                            
                            logger.info(f"WriterAgent: Generating content via blog service API...")
                            generate_response = await client.post(
                                f"{BLOG_SERVICE_URL}/blogs/{blog_id}/generate",
                                json=generate_data
                            )
                            
                            if generate_response.status_code == 200:
                                generate_result = generate_response.json()
                                if generate_result.get("success"):
                                    content = generate_result["data"]["content"]
                                    version = generate_result["data"]["version"]
                                    logger.info(f"WriterAgent: Generated content (version {version}) for blog {blog_id}")
                                    
                                    # Calculate processing time
                                    end_time = datetime.utcnow()
                                    processing_time_ms = int((end_time - start_time).total_seconds() * 1000)
                                    
                                    result_data = {
                                        "content": content,
                                        "word_count": len(content.split()),
                                        "char_count": len(content),
                                        "model": "ibm/granite-3-8b-instruct",
                                        "processing_time_ms": processing_time_ms,
                                        "blog_id": blog_id,
                                        "blog_status": "draft",
                                        "blog_title": title,
                                        "version": version
                                    }
                                    
                                    return AgentResult(
                                        success=True,
                                        data=result_data,
                                        metadata={
                                            "prompt": prompt,
                                            "tone": tone,
                                            "blog_created": True
                                        }
                                    )
                                else:
                                    error_msg = generate_result.get("message", "Content generation failed")
                                    logger.error(f"WriterAgent: {error_msg}")
                                    return AgentResult(
                                        success=False,
                                        error=error_msg
                                    )
                            else:
                                error_msg = f"Blog service returned status {generate_response.status_code}"
                                logger.error(f"WriterAgent: {error_msg}")
                                return AgentResult(
                                    success=False,
                                    error=error_msg
                                )
                    else:
                        error_msg = f"Failed to create blog: {create_response.status_code}"
                        logger.error(f"WriterAgent: {error_msg}")
                        return AgentResult(
                            success=False,
                            error=error_msg
                        )
                        
            except Exception as api_error:
                logger.error(f"WriterAgent: API call failed: {str(api_error)}")
                return AgentResult(
                    success=False,
                    error=f"API call failed: {str(api_error)}"
                )
        
        except Exception as e:
            logger.error(f"WriterAgent: Failed to generate content: {str(e)}")
            return AgentResult(
                success=False,
                error=str(e)
            )
        
        # Fallback return (should never reach here)
        return AgentResult(
            success=False,
            error="Unexpected execution path"
        )

# Made with Bob
