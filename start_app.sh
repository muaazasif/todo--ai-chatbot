#!/bin/bash

# Set the Python path
export PYTHONPATH="/app:$PYTHONPATH"

# Run the migrations
alembic upgrade head

# Run the test server to verify basic setup works
exec python test_server.py