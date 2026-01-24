#!/usr/bin/env python3

import os
import sys

# Add the app directory to the Python path so we can import backend
sys.path.insert(0, '/app')

# Import and run the application
import uvicorn
from backend.main import app

port = int(os.environ.get("PORT", 8000))
print(f"PORT environment variable value: {os.environ.get('PORT')}")
print(f"Using port: {port}")

uvicorn.run(app, host="0.0.0.0", port=port)