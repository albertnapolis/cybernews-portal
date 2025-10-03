#!/usr/bin/env python
"""
Server management utility for Cybersecurity News Portal
"""

import sys
import os
import subprocess
import platform
import time

def find_process_using_port(port=8000):
    """Find process ID using the specified port"""
    system = platform.system()

    if system == "Windows":
        cmd = f"netstat -ano | findstr :{port}"
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)

        if result.stdout:
            lines = result.stdout.strip().split('\n')
            for line in lines:
                if 'LISTENING' in line:
                    parts = line.split()
                    pid = parts[-1]
                    return pid
    else:
        # Linux/Mac
        cmd = f"lsof -ti:{port}"
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        if result.stdout:
            return result.stdout.strip()

    return None

def kill_process(pid):
    """Kill process by PID"""
    system = platform.system()

    if system == "Windows":
        cmd = f"taskkill //F //PID {pid}"
    else:
        cmd = f"kill -9 {pid}"

    subprocess.run(cmd, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    print(f"Killed process {pid}")

def stop_server():
    """Stop the server if it's running"""
    pid = find_process_using_port(8000)
    if pid:
        print(f"Found server running on port 8000 (PID: {pid})")
        kill_process(pid)
        time.sleep(1)
        print("Server stopped successfully")
    else:
        print("No server found running on port 8000")

def start_server():
    """Start the server"""
    print("Starting Cybersecurity News Portal Backend...")

    # Add current directory to path
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

    from main import app
    import uvicorn

    try:
        uvicorn.run(app, host="0.0.0.0", port=8000)
    except Exception as e:
        print(f"Error starting server: {e}")
        sys.exit(1)

def restart_server():
    """Stop and start the server"""
    stop_server()
    time.sleep(2)
    start_server()

def main():
    """Main entry point"""
    if len(sys.argv) < 2:
        print("Usage: python manage_server.py [start|stop|restart]")
        sys.exit(1)

    command = sys.argv[1].lower()

    if command == "start":
        # Check if already running
        pid = find_process_using_port(8000)
        if pid:
            print(f"Server already running on port 8000 (PID: {pid})")
            print("Use 'python manage_server.py restart' to restart")
            sys.exit(1)
        start_server()
    elif command == "stop":
        stop_server()
    elif command == "restart":
        restart_server()
    else:
        print(f"Unknown command: {command}")
        print("Usage: python manage_server.py [start|stop|restart]")
        sys.exit(1)

if __name__ == "__main__":
    main()