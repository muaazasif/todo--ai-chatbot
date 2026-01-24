#!/usr/bin/env python3

import os
import sys

# The main.py file is directly in /app since we copied backend/contents to /
# So we don't need to change directory, just add /app to the path
sys.path.insert(0, '/app')

# Import and run the application
import uvicorn
from main import app

port = int(os.environ.get("PORT", 8000))
print(f"PORT environment variable value: {os.environ.get('PORT')}")
print(f"Using port: {port}")

uvicorn.run(app, host="0.0.0.0", port=port)