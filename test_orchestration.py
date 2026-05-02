#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test script for the orchestration service
"""
import asyncio
import httpx
import json
from datetime import datetime

# Service URLs
ORCHESTRATION_URL = "http://localhost:8004"
API_GATEWAY_URL = "http://localhost:8000"

async def test_orchestration_health():
    """Test orchestration service health"""
    print("\n=== Testing Orchestration Service Health ===")
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{ORCHESTRATION_URL}/health")
            print(f"Status: {response.status_code}")
            print(f"Response: {response.json()}")
            return response.status_code == 200
    except Exception as e:
        print(f"[ERROR] Error: {e}")
        return False

async def test_list_agents():
    """Test listing registered agents"""
    print("\n=== Testing Agent Registration ===")
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{ORCHESTRATION_URL}/agents")
            data = response.json()
            print(f"Status: {response.status_code}")
            print(f"Registered agent classes: {data.get('data', {}).get('agent_classes', [])}")
            print(f"Agent instances: {len(data.get('data', {}).get('agent_instances', {}))}")
            return response.status_code == 200
    except Exception as e:
        print(f"[ERROR] Error: {e}")
        return False

async def test_blog_generation():
    """Test blog generation through orchestration"""
    print("\n=== Testing Blog Generation Pipeline ===")
    try:
        request_data = {
            "prompt": "Write a blog post about the benefits of AI in software development",
            "tone": "professional"
        }
        
        print(f"Sending request: {json.dumps(request_data, indent=2)}")
        
        async with httpx.AsyncClient(timeout=60.0) as client:
            response = await client.post(
                f"{ORCHESTRATION_URL}/blog/generate",
                json=request_data
            )
            
            print(f"Status: {response.status_code}")
            data = response.json()
            
            if data.get("success"):
                print("[SUCCESS] Blog generation successful!")
                pipeline_data = data.get("data", {})
                print(f"Pipeline state: {pipeline_data.get('state')}")
                print(f"Steps completed: {pipeline_data.get('current_step') + 1}/{pipeline_data.get('total_steps')}")
                print(f"Duration: {pipeline_data.get('duration_seconds', 0):.2f}s")
                
                # Show step details
                steps = pipeline_data.get("steps", [])
                for i, step in enumerate(steps):
                    print(f"\nStep {i+1}: {step.get('agent_name')}")
                    print(f"  - Completed: {step.get('completed')}")
                    print(f"  - Success: {step.get('success')}")
                
                return True
            else:
                print(f"[FAIL] Blog generation failed: {data.get('message')}")
                return False
                
    except Exception as e:
        print(f"[ERROR] Error: {e}")
        return False

async def test_via_api_gateway():
    """Test orchestration through API gateway"""
    print("\n=== Testing via API Gateway ===")
    try:
        request_data = {
            "prompt": "Write a short blog about Python best practices",
            "tone": "casual"
        }
        
        async with httpx.AsyncClient(timeout=60.0) as client:
            response = await client.post(
                f"{API_GATEWAY_URL}/api/blogs/generate-orchestrated",
                json=request_data
            )
            
            print(f"Status: {response.status_code}")
            data = response.json()
            
            if data.get("success"):
                print("[SUCCESS] API Gateway integration successful!")
                return True
            else:
                print(f"[FAIL] API Gateway integration failed")
                return False
                
    except Exception as e:
        print(f"[ERROR] Error: {e}")
        return False

async def test_list_pipelines():
    """Test listing pipelines"""
    print("\n=== Testing Pipeline Listing ===")
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{ORCHESTRATION_URL}/pipelines")
            data = response.json()
            print(f"Status: {response.status_code}")
            pipelines = data.get("data", {})
            print(f"Total pipelines: {len(pipelines)}")
            
            for pipeline_id, pipeline_info in pipelines.items():
                print(f"\nPipeline: {pipeline_info.get('name')}")
                print(f"  - ID: {pipeline_id}")
                print(f"  - State: {pipeline_info.get('state')}")
                print(f"  - Steps: {pipeline_info.get('total_steps')}")
            
            return response.status_code == 200
    except Exception as e:
        print(f"[ERROR] Error: {e}")
        return False

async def main():
    """Run all tests"""
    print("=" * 60)
    print("ORCHESTRATION SERVICE TEST SUITE")
    print("=" * 60)
    
    results = []
    
    # Test 1: Health check
    results.append(("Health Check", await test_orchestration_health()))
    
    # Test 2: List agents
    results.append(("Agent Registration", await test_list_agents()))
    
    # Test 3: Blog generation
    results.append(("Blog Generation", await test_blog_generation()))
    
    # Test 4: List pipelines
    results.append(("Pipeline Listing", await test_list_pipelines()))
    
    # Test 5: API Gateway integration
    results.append(("API Gateway Integration", await test_via_api_gateway()))
    
    # Summary
    print("\n" + "=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "[PASS]" if result else "[FAIL]"
        print(f"{status} - {test_name}")
    
    print(f"\nTotal: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n[SUCCESS] All tests passed!")
    else:
        print(f"\n[WARNING] {total - passed} test(s) failed")

if __name__ == "__main__":
    asyncio.run(main())

# Made with Bob
