#!/bin/bash

# Set the Python path
export PYTHONPATH="/app:$PYTHONPATH"

# Run the migrations
alembic upgrade head

# Run the application directly with uvicorn without reload
exec uvicorn main:app --host 0.0.0.0 --port ${PORT:-8000} --reload=false