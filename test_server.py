#!/usr/bin/env python3

import os
import sys

# Add the current directory to Python path
sys.path.insert(0, '/app')

# Set environment variable to help with imports
os.environ['PYTHONPATH'] = '/app'

# Create a minimal FastAPI app to test if the basic setup works
from fastapi import FastAPI
import uvicorn

app = FastAPI(title="Test App")

@app.get("/")
def read_root():
    return {"Hello": "World", "status": "working"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    print(f"Starting test server on port {port}")
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=port,
        reload=False,
        log_level="info"
    )