#!/usr/bin/env python3

import os
import sys

# Add the current directory to Python path
sys.path.insert(0, '/app')

# Set environment variable to help with imports
os.environ['PYTHONPATH'] = '/app'

# Import and run the application directly without subprocess
import uvicorn
import importlib.util

# Load the main module directly from file
spec = importlib.util.spec_from_file_location("main", "/app/main.py")
main_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(main_module)

# Get the app instance
app = main_module.app

# Get the port from environment
port = int(os.environ.get("PORT", 8000))
print(f"PORT environment variable value: {os.environ.get('PORT')}")
print(f"Using port: {port}")

# Run the app with uvicorn
uvicorn.run(
    app,
    host="0.0.0.0",
    port=port,
    log_level="info"
)