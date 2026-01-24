#!/usr/bin/env python3

import os
import sys
import subprocess

# Set environment variable to help with imports
os.environ['PYTHONPATH'] = '/app'

# Execute the main application directly using uvicorn
port = int(os.environ.get("PORT", 8000))
print(f"PORT environment variable value: {os.environ.get('PORT')}")
print(f"Using port: {port}")

# Run uvicorn directly on the main module
cmd = [
    "uvicorn",
    "main:app",
    "--host", "0.0.0.0",
    "--port", str(port),
    "--forwarded-allow-ips", "*"  # In case behind proxy
]

os.execvp("uvicorn", cmd)