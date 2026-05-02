"""
IBM watsonx.ai Granite LLM Client
"""
from ibm_watsonx_ai.foundation_models import ModelInference
from ibm_watsonx_ai.metanames import GenTextParamsMetaNames as GenParams
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from typing import Optional, Dict, Any
import logging
import json

from .config import granite_config

logger = logging.getLogger(__name__)


class GraniteClient:
    """Client for IBM watsonx.ai foundation models"""
    
    def __init__(self, config: Optional[Any] = None):
        """
        Initialize watsonx client
        
        Args:
            config: Optional GraniteConfig instance. If None, uses global config.
        """
        self.config = config or granite_config
        
        if not self.config.validate_credentials():
            raise ValueError(
                "IBM watsonx credentials not configured. "
                "Set IBM_CLOUD_API_KEY and WATSONX_PROJECT_ID in .env"
            )
        
        # Initialize IBM watsonx.ai model
        self.model = self._initialize_model()
        logger.info(f"watsonx client initialized with model: {self.config.model_id}")
    
    def _initialize_model(self) -> ModelInference:
        """Initialize the watsonx model"""
        try:
            # Disable retries to fail fast on rate limits
            model = ModelInference(
                model_id=self.config.model_id,
                params={
                    GenParams.MAX_NEW_TOKENS: self.config.max_new_tokens,
                    GenParams.TEMPERATURE: self.config.temperature,
                    GenParams.TOP_P: self.config.top_p,
                    GenParams.TOP_K: self.config.top_k,
                    GenParams.REPETITION_PENALTY: self.config.repetition_penalty,
                },
                credentials={
                    "apikey": self.config.api_key,
                    "url": self.config.url
                },
                project_id=self.config.project_id,
                verify=False  # Disable SSL verification if needed
            )
            return model
        except Exception as e:
            logger.error(f"Failed to initialize watsonx model: {str(e)}")
            raise
    
    def generate(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        max_tokens: Optional[int] = None,
        temperature: Optional[float] = None
    ) -> str:
        """
        Generate text using watsonx model
        
        Args:
            prompt: User prompt
            system_prompt: Optional system prompt for context
            max_tokens: Override default max_new_tokens
            temperature: Override default temperature
            
        Returns:
            Generated text
        """
        try:
            # Construct full prompt with system context
            full_prompt = self._construct_prompt(prompt, system_prompt)
            
            # Override parameters if provided
            params = {}
            if max_tokens:
                params[GenParams.MAX_NEW_TOKENS] = max_tokens
            if temperature is not None:
                params[GenParams.TEMPERATURE] = temperature
            
            # Generate text
            logger.info(f"Generating with watsonx (prompt length: {len(full_prompt)} chars)")
            
            if params:
                # Create temporary model with custom params
                temp_model = ModelInference(
                    model_id=self.config.model_id,
                    params={
                        GenParams.MAX_NEW_TOKENS: params.get(GenParams.MAX_NEW_TOKENS, self.config.max_new_tokens),
                        GenParams.TEMPERATURE: params.get(GenParams.TEMPERATURE, self.config.temperature),
                        GenParams.TOP_P: self.config.top_p,
                        GenParams.TOP_K: self.config.top_k,
                        GenParams.REPETITION_PENALTY: self.config.repetition_penalty,
                    },
                    credentials={"apikey": self.config.api_key, "url": self.config.url},
                    project_id=self.config.project_id
                )
                response = temp_model.generate_text(prompt=full_prompt)
            else:
                response = self.model.generate_text(prompt=full_prompt)
            
            # Ensure response is a string
            if isinstance(response, dict):
                response = response.get('results', [{}])[0].get('generated_text', '')
            elif isinstance(response, list):
                response = response[0] if response else ''
            
            logger.info(f"watsonx generation successful (response length: {len(response)} chars)")
            return str(response)
            
        except Exception as e:
            error_msg = str(e)
            # Check for rate limit error
            if "429" in error_msg or "Too Many Requests" in error_msg:
                logger.error("Rate limit exceeded. Please wait 5 minutes before trying again.")
                raise ValueError(
                    "IBM watsonx.ai rate limit exceeded. "
                    "Please wait 5 minutes before generating more content. "
                    "This is normal with the free tier plan."
                )
            logger.error(f"watsonx generation failed: {error_msg}")
            raise
    
    def generate_structured(
        self,
        prompt: str,
        schema: Dict[str, Any],
        system_prompt: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Generate structured JSON output
        
        Args:
            prompt: User prompt
            schema: JSON schema for expected output
            system_prompt: Optional system prompt
            
        Returns:
            Parsed JSON object
        """
        response = ""
        try:
            # Add JSON schema instruction to prompt
            json_instruction = (
                f"\n\nRespond with valid JSON matching this schema:\n"
                f"```json\n{json.dumps(schema, indent=2)}\n```\n"
                f"Return ONLY the JSON object, no additional text."
            )
            
            full_prompt = prompt + json_instruction
            
            # Generate response
            response = self.generate(full_prompt, system_prompt)
            
            # Extract JSON from response (handle markdown code blocks)
            json_text = self._extract_json(response)
            
            # Parse JSON
            result = json.loads(json_text)
            logger.info("Structured generation successful")
            return result
            
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse JSON response: {str(e)}")
            logger.error(f"Response was: {response}")
            raise ValueError(f"Invalid JSON response from watsonx: {str(e)}")
        except Exception as e:
            logger.error(f"Structured generation failed: {str(e)}")
            raise
    
    def _construct_prompt(self, prompt: str, system_prompt: Optional[str] = None) -> str:
        """Construct full prompt with system context"""
        if system_prompt:
            return f"{system_prompt}\n\n{prompt}"
        return prompt
    
    def _extract_json(self, text: str) -> str:
        """Extract JSON from text (handles markdown code blocks)"""
        # Remove markdown code blocks if present
        if "```json" in text:
            start = text.find("```json") + 7
            end = text.find("```", start)
            return text[start:end].strip()
        elif "```" in text:
            start = text.find("```") + 3
            end = text.find("```", start)
            return text[start:end].strip()
        return text.strip()
    
    def test_connection(self) -> bool:
        """Test connection to IBM watsonx.ai"""
        try:
            response = self.generate("Say 'Hello from Granite!'", max_tokens=50)
            return "Granite" in response or "Hello" in response
        except Exception as e:
            logger.error(f"Connection test failed: {str(e)}")
            return False


# Global client instance
_granite_client: Optional[GraniteClient] = None


def get_granite_client() -> GraniteClient:
    """Get or create global Granite client instance"""
    global _granite_client
    if _granite_client is None:
        _granite_client = GraniteClient()
    return _granite_client

# Made with Bob
