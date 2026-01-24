#!/bin/bash

# Set the Python path
export PYTHONPATH="/app:$PYTHONPATH"

# Run the migrations
alembic upgrade head

# Run the application directly with uvicorn without reload or workers
exec python -c "
import os
import sys
sys.path.insert(0, '/app')
os.environ['PYTHONPATH'] = '/app'

# Load and run the app directly
import uvicorn
from main import app

port = int(os.environ.get('PORT', 8000))
print(f'Starting server on port {port}')

uvicorn.run(
    app,
    host='0.0.0.0',
    port=port,
    reload=False,
    log_level='info'
)
"