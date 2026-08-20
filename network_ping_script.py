import socket
import requests
import time
import random
import os
import signal

TARGET_IP = "20.127.108.146"

# Mix web ports with admin ports for a combo of allowed and denied traffic
PORTS_TO_SCAN = [22, 23, 80, 443, 3389, 8080, 27017]

def force_exit(sig, frame):
    # Override loop when Ctrl+C is pressed
    print("\nQuit signal received. Shutting down simulator.")
    os._exit(0)

# Register the signal handler to listen for Ctrl+C (SIGINT)
signal.signal(signal.SIGINT, force_exit)

def simulate_heavy_traffic():
    """Simulates an allowed connection moving data (Spikes the C & E charts)"""
    try:
        print(f"Sending HTTP request to {TARGET_IP} (Simulating Web User)")
        # Timeout so it doesn't hang if the port is actually blocked
        requests.get(f"http://{TARGET_IP}", timeout=2)
    except requests.exceptions.RequestException:
        pass 

def simulate_port_scan(port):
    # Simulates a blocked connection attempt (Spikes the B & D charts)
    try:
        print(f"Probing port {port} on {TARGET_IP} (Simulating Port Scan)")
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(0.5)
        sock.connect_ex((TARGET_IP, port))
        sock.close()
    except Exception:
        pass

print(f"Starting Network Simulator against {TARGET_IP}.")
print("Press Ctrl+C to stop.")

while True:
    # Randomized behavior: 50% chance of web traffic, 50% chance of port scanning
    action = random.choices(["web", "scan"], weights=[0.5, 0.5])[0]
    
    if action == "web":
        simulate_heavy_traffic()
    else:
        port = random.choice(PORTS_TO_SCAN)
        simulate_port_scan(port)
        
    # Sleep for a random time period to simulate unpredictable traffic
    time.sleep(random.uniform(0.1, 1.0))