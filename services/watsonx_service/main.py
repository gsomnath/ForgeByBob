"""
IBM watsonx.ai Service - FastAPI microservice for Granite LLM
"""
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional, Dict, Any
import logging

from .granite_client import get_granite_client, GraniteClient
from .config import granite_config

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="IBM watsonx.ai Service",
    description="Microservice for IBM Granite LLM text generation",
    version="1.0.0"
)

# Global client instance
granite_client: Optional[GraniteClient] = None


class GenerateRequest(BaseModel):
    """Request model for text generation"""
    prompt: str
    system_prompt: Optional[str] = None
    max_tokens: Optional[int] = None
    temperature: Optional[float] = None


class GenerateResponse(BaseModel):
    """Response model for text generation"""
    success: bool
    text: str
    model: str
    tokens_used: Optional[int] = None


class StructuredGenerateRequest(BaseModel):
    """Request model for structured JSON generation"""
    prompt: str
    json_schema: Dict[str, Any]
    system_prompt: Optional[str] = None


class StructuredGenerateResponse(BaseModel):
    """Response model for structured generation"""
    success: bool
    data: Dict[str, Any]
    model: str


class HealthResponse(BaseModel):
    """Health check response"""
    status: str
    service: str
    model: str
    credentials_valid: bool


@app.on_event("startup")
async def startup_event():
    """Initialize Granite client on startup"""
    global granite_client
    try:
        granite_client = get_granite_client()
        logger.info("IBM watsonx.ai service started successfully")
    except Exception as e:
        logger.error(f"Failed to initialize Granite client: {str(e)}")
        # Don't fail startup, allow health check to report the issue


@app.get("/", response_model=HealthResponse)
async def root():
    """Root endpoint with service information"""
    return HealthResponse(
        status="running",
        service="IBM watsonx.ai Service",
        model=granite_config.model_id,
        credentials_valid=granite_config.validate_credentials()
    )


@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint"""
    try:
        if granite_client is None:
            return HealthResponse(
                status="error",
                service="IBM watsonx.ai Service",
                model=granite_config.model_id,
                credentials_valid=False
            )
        
        # Test connection
        connection_ok = granite_client.test_connection()
        
        return HealthResponse(
            status="healthy" if connection_ok else "unhealthy",
            service="IBM watsonx.ai Service",
            model=granite_config.model_id,
            credentials_valid=granite_config.validate_credentials()
        )
    except Exception as e:
        logger.error(f"Health check failed: {str(e)}")
        return HealthResponse(
            status="error",
            service="IBM watsonx.ai Service",
            model=granite_config.model_id,
            credentials_valid=False
        )


@app.post("/generate", response_model=GenerateResponse)
async def generate_text(request: GenerateRequest):
    """
    Generate text using IBM Granite model
    
    Args:
        request: Generation request with prompt and optional parameters
        
    Returns:
        Generated text response
    """
    try:
        if granite_client is None:
            raise HTTPException(
                status_code=503,
                detail="IBM watsonx client not initialized. Check credentials."
            )
        
        # Generate text
        text = granite_client.generate(
            prompt=request.prompt,
            system_prompt=request.system_prompt,
            max_tokens=request.max_tokens,
            temperature=request.temperature
        )
        
        return GenerateResponse(
            success=True,
            text=text,
            model=granite_config.model_id,
            tokens_used=None  # IBM SDK doesn't provide token count in response
        )
        
    except Exception as e:
        logger.error(f"Text generation failed: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/generate/structured", response_model=StructuredGenerateResponse)
async def generate_structured(request: StructuredGenerateRequest):
    """
    Generate structured JSON output using IBM Granite model
    
    Args:
        request: Structured generation request with prompt and schema
        
    Returns:
        Parsed JSON object matching the schema
    """
    try:
        if granite_client is None:
            raise HTTPException(
                status_code=503,
                detail="IBM watsonx client not initialized. Check credentials."
            )
        
        # Generate structured output
        data = granite_client.generate_structured(
            prompt=request.prompt,
            schema=request.json_schema,
            system_prompt=request.system_prompt
        )
        
        return StructuredGenerateResponse(
            success=True,
            data=data,
            model=granite_config.model_id
        )
        
    except Exception as e:
        logger.error(f"Structured generation failed: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/config")
async def get_config():
    """Get current configuration (without sensitive data)"""
    return {
        "model_id": granite_config.model_id,
        "url": granite_config.url,
        "max_new_tokens": granite_config.max_new_tokens,
        "temperature": granite_config.temperature,
        "top_p": granite_config.top_p,
        "top_k": granite_config.top_k,
        "repetition_penalty": granite_config.repetition_penalty,
        "credentials_configured": granite_config.validate_credentials()
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8005)

# Made with Bob