# Simple app.py file for deployment auto-detection
# This file allows deployment platforms to auto-detect the FastAPI application

import sys
import os

# Add backend to the path so imports work correctly
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

# Set default database URL if not provided
if 'DATABASE_URL' not in os.environ:
    os.environ['DATABASE_URL'] = 'sqlite:///./todo_chatbot.db'

# Import the app from the main module
from main import app

# This allows deployment platforms to auto-detect the FastAPI app
# as 'app' in the 'app' module