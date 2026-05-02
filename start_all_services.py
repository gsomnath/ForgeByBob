#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script to start all microservices for the Blog Writer application.
"""
import subprocess
import time
import sys
import socket
import psutil
from pathlib import Path

# Constants
SERVICE_START_DELAY = 1  # seconds between service starts
SERVICE_STARTUP_TIME = 3  # seconds to wait for service initialization
PORT_RELEASE_TIMEOUT = 10  # seconds to wait for port release
PROCESS_TERMINATION_TIMEOUT = 5  # seconds to wait for graceful termination

def is_port_in_use(port):
    """Check if a port is in use."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(('localhost', port)) == 0

def kill_process_on_port(port):
    """Kill any process using the specified port."""
    try:
        for proc in psutil.process_iter(['pid', 'name', 'connections']):
            try:
                connections = proc.connections()
                for conn in connections:
                    if conn.laddr.port == port:
                        print(f"  Found process {proc.info['name']} (PID: {proc.info['pid']}) on port {port}")
                        proc.kill()
                        print(f"  Killed process on port {port}")
                        return True
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                pass
    except Exception as e:
        print(f"  Error checking port {port}: {e}")
    return False

def stop_all_python_services():
    """Stop all Python processes that might be running services."""
    print("=== Stopping Existing Services ===")
    
    # Kill all python processes (aggressive approach)
    try:
        if sys.platform == "win32":
            subprocess.run(["taskkill", "/F", "/IM", "python.exe", "/T"],
                         capture_output=True, check=False)
            print("Stopped all Python processes")
        else:
            subprocess.run(["pkill", "-9", "python"],
                         capture_output=True, check=False)
            print("Stopped all Python processes")
    except Exception as e:
        print(f"Warning: Could not kill Python processes: {e}")
    
    # Wait for processes to terminate
    time.sleep(3)

def wait_for_port_release(port, timeout=PORT_RELEASE_TIMEOUT):
    """Wait for a port to be released."""
    print(f"  Waiting for port {port} to be released...")
    start_time = time.time()
    
    while is_port_in_use(port):
        if time.time() - start_time > timeout:
            print(f"  [WARNING] Port {port} still in use after {timeout}s")
            # Try to kill the process one more time
            kill_process_on_port(port)
            time.sleep(2)
            if is_port_in_use(port):
                print(f"  [ERROR] Could not release port {port}")
                return False
        time.sleep(0.5)
    
    print(f"  [OK] Port {port} is now available")
    return True

def start_service(service_name, port):
    """Start a single service."""
    try:
        # Check if port is in use
        if is_port_in_use(port):
            print(f"[WARNING] Port {port} is in use for {service_name}")
            kill_process_on_port(port)
            if not wait_for_port_release(port):
                print(f"[ERROR] Cannot start {service_name} - port {port} is still in use")
                return None
        
        print(f"Starting {service_name} on port {port}...")
        
        # Start the service in a new process
        process = subprocess.Popen([
            sys.executable, "-m", f"services.{service_name}.main"
        ], cwd=Path(__file__).parent)
        
        # Give the service time to start
        time.sleep(SERVICE_STARTUP_TIME)
        
        # Verify the service started
        if is_port_in_use(port):
            print(f"[OK] {service_name} started (PID: {process.pid})")
            return process
        else:
            print(f"[WARNING] {service_name} may not have started properly")
            return process
        
    except Exception as e:
        print(f"[ERROR] Failed to start {service_name}: {e}")
        return None

def verify_ports_available(services):
    """Verify all required ports are available."""
    print("\n=== Checking Ports ===")
    for service_name, port in services:
        if is_port_in_use(port):
            print(f"[WARNING] Port {port} ({service_name}) is still in use")
            kill_process_on_port(port)
            wait_for_port_release(port)

def start_all_services(services):
    """Start all services and return their processes."""
    print("\n=== Starting Services ===")
    processes = []
    
    for service_name, port in services:
        process = start_service(service_name, port)
        if process:
            processes.append((service_name, process))
        time.sleep(SERVICE_START_DELAY)  # Stagger service starts to avoid port conflicts
    
    return processes

def display_service_urls(services):
    """Display URLs for all running services."""
    print("\n=== All Services Started ===")
    for service_name, port in services:
        # Format service name for display
        display_name = service_name.replace('_', ' ').title()
        print(f"{display_name}: http://localhost:{port}")
    
    # Special case for web interface
    print("Web Interface: http://localhost:8003")
    print("\nPress Ctrl+C to stop all services...")

def cleanup_services(processes):
    """Gracefully stop all service processes."""
    print("\n=== Stopping Services ===")
    for service_name, process in processes:
        try:
            process.terminate()
            process.wait(timeout=PROCESS_TERMINATION_TIMEOUT)
            print(f"[OK] Stopped {service_name}")
        except subprocess.TimeoutExpired:
            process.kill()
            print(f"[OK] Force stopped {service_name}")
        except Exception as e:
            print(f"[ERROR] Error stopping {service_name}: {e}")

def main():
    """Start all services."""
    print("=== Blog Writer Application Startup ===\n")
    
    # Stop existing services
    stop_all_python_services()
    
    # Define services configuration
    services = [
        ("settings_service", 8002),
        ("api_gateway", 8000),
        ("blog_service", 8001),
        ("ui_service", 8003),
    ]
    
    # Verify ports are available
    verify_ports_available(services)
    
    # Start all services
    processes = start_all_services(services)
    
    # Display service information
    display_service_urls(services)
    
    # Wait for shutdown signal
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        cleanup_services(processes)

if __name__ == "__main__":
    main()
