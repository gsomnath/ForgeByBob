"""
Test script for Granite client
"""
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.append(str(project_root))

from services.watsonx_service.granite_client import GraniteClient
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def test_basic_generation():
    """Test basic text generation"""
    print("\n" + "="*60)
    print("TEST 1: Basic Text Generation")
    print("="*60)
    
    client = GraniteClient()
    
    prompt = "Write a short introduction about artificial intelligence in 2-3 sentences."
    
    print(f"\nPrompt: {prompt}")
    print("\nGenerating...")
    
    response = client.generate(prompt)
    
    print(f"\nResponse:\n{response}")
    print("\n✓ Test passed!")


def test_system_prompt():
    """Test generation with system prompt"""
    print("\n" + "="*60)
    print("TEST 2: Generation with System Prompt")
    print("="*60)
    
    client = GraniteClient()
    
    system_prompt = "You are a professional blog writer with expertise in technology."
    prompt = "Write a blog introduction about cloud computing."
    
    print(f"\nSystem Prompt: {system_prompt}")
    print(f"User Prompt: {prompt}")
    print("\nGenerating...")
    
    response = client.generate(prompt, system_prompt=system_prompt)
    
    print(f"\nResponse:\n{response}")
    print("\n✓ Test passed!")


def test_structured_output():
    """Test structured JSON generation"""
    print("\n" + "="*60)
    print("TEST 3: Structured JSON Output")
    print("="*60)
    
    client = GraniteClient()
    
    prompt = "Create a blog post outline about machine learning."
    schema = {
        "title": "string",
        "sections": ["string"],
        "estimated_words": "number"
    }
    
    print(f"\nPrompt: {prompt}")
    print(f"Expected Schema: {schema}")
    print("\nGenerating...")
    
    response = client.generate_structured(prompt, schema)
    
    print(f"\nResponse:\n{response}")
    print("\n✓ Test passed!")


def test_connection():
    """Test connection to watsonx.ai"""
    print("\n" + "="*60)
    print("TEST 4: Connection Test")
    print("="*60)
    
    client = GraniteClient()
    
    print("\nTesting connection to IBM watsonx.ai...")
    
    success = client.test_connection()
    
    if success:
        print("\n✓ Connection successful!")
    else:
        print("\n✗ Connection failed!")
        sys.exit(1)


if __name__ == "__main__":
    try:
        test_connection()
        test_basic_generation()
        test_system_prompt()
        test_structured_output()
        
        print("\n" + "="*60)
        print("ALL TESTS PASSED! ✓")
        print("="*60)
        print("\nGranite client is ready to use!")
        
    except Exception as e:
        print(f"\n✗ Test failed: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

# Made with Bob
