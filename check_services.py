"""
Check if all services are running
"""
import socket
import sys

# Set UTF-8 encoding for Windows console
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

def check_port(port, service_name):
    """Check if a port is in use (service is running)"""
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    result = sock.connect_ex(('localhost', port))
    sock.close()
    
    if result == 0:
        print(f"[OK] {service_name} is RUNNING on port {port}")
        return True
    else:
        print(f"[X] {service_name} is NOT running on port {port}")
        return False

print("=" * 60)
print("Checking ForgeByBob Services Status")
print("=" * 60)

services = [
    (8000, "API Gateway"),
    (8001, "Blog Service"),
    (8002, "Settings Service"),
    (8003, "UI Service (Web Interface)"),
]

all_running = True
for port, name in services:
    if not check_port(port, name):
        all_running = False

print("=" * 60)
if all_running:
    print("[SUCCESS] ALL SERVICES ARE RUNNING!")
    print("\nOpen your browser and go to:")
    print("   http://localhost:8003")
    print("\nYou can now use the application!")
else:
    print("[WARNING] Some services are not running.")
    print("\nTo start services, run:")
    print("   python start_all_services.py")
print("=" * 60)

# Made with Bob
