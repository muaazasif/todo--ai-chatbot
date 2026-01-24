#!/usr/bin/env python3

import os
import sys

# Change to the backend directory to run the app from there
os.chdir('/app/backend')

# Add the current directory to the Python path
sys.path.insert(0, '/app/backend')

# Import and run the application
import uvicorn
from main import app

port = int(os.environ.get("PORT", 8000))
print(f"PORT environment variable value: {os.environ.get('PORT')}")
print(f"Using port: {port}")

uvicorn.run(app, host="0.0.0.0", port=port)