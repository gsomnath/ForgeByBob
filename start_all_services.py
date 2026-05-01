#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script to start all microservices for the Blog Writer application.
"""
import subprocess
import time
import sys
from pathlib import Path

def start_service(service_name, port):
    """Start a single service."""
    try:
        print(f"Starting {service_name} on port {port}...")
        
        # Start the service in a new process
        process = subprocess.Popen([
            sys.executable, "-m", f"services.{service_name}.main"
        ], cwd=Path(__file__).parent)
        
        # Give the service time to start
        time.sleep(2)
        
        print(f"[OK] {service_name} started (PID: {process.pid})")
        return process
        
    except Exception as e:
        print(f"[ERROR] Failed to start {service_name}: {e}")
        return None

def main():
    """Start all services."""
    print("=== Blog Writer Application Startup ===")
    
    services = [
        ("settings_service", 8002),
        ("api_gateway", 8000),
        ("blog_service", 8001),
        ("ui_service", 8003),
    ]
    
    processes = []
    
    for service_name, port in services:
        process = start_service(service_name, port)
        if process:
            processes.append((service_name, process))
    
    print("\n=== All Services Started ===")
    print("Settings Service: http://localhost:8002")
    print("API Gateway: http://localhost:8000")
    print("Blog Service: http://localhost:8001")
    print("UI Service: http://localhost:8003")
    print("Web Interface: http://localhost:8003")
    print("\nPress Ctrl+C to stop all services...")
    
    try:
        # Keep the script running
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n=== Stopping Services ===")
        for service_name, process in processes:
            try:
                process.terminate()
                print(f"[OK] Stopped {service_name}")
            except:
                print(f"[ERROR] Failed to stop {service_name}")

if __name__ == "__main__":
    main()
