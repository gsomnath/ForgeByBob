#!/usr/bin/env python3
"""Stop all services by killing processes on their ports."""
import psutil
import time

PORTS = [8000, 8001, 8002, 8003, 8004]

def kill_process_on_port(port):
    """Kill any process using the specified port."""
    killed = False
    for proc in psutil.process_iter(['pid', 'name']):
        try:
            for conn in proc.connections():
                if conn.laddr.port == port:
                    print(f"Killing {proc.info['name']} (PID: {proc.info['pid']}) on port {port}")
                    proc.kill()
                    killed = True
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    return killed

print("=== Stopping All Services ===")
for port in PORTS:
    if kill_process_on_port(port):
        print(f"[OK] Stopped service on port {port}")
    else:
        print(f"[INFO] No service running on port {port}")

print("\nWaiting for processes to terminate...")
time.sleep(2)
print("[OK] All services stopped!")

# Made with Bob
