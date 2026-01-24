#!/usr/bin/env python3

import os
import sys

# Set environment variable to help with imports
os.environ['PYTHONPATH'] = '/app'

# Execute the main application directly using uvicorn
port = int(os.environ.get("PORT", 8000))
print(f"PORT environment variable value: {os.environ.get('PORT')}")
print(f"Using port: {port}")

# Use os.system to run uvicorn which handles imports differently
import subprocess
result = subprocess.run([
    "uvicorn",
    "main:app",
    "--host", "0.0.0.0",
    "--port", str(port),
    "--reload", "false"  # Disable reload in production
])

sys.exit(result.returncode)