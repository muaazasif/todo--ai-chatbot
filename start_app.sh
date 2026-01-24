#!/bin/bash

# Set database URL
export DATABASE_URL=${DATABASE_URL:-"sqlite:///./todo_chatbot.db"}

# Change to the app directory where alembic.ini is located for migrations
cd /app

# Run the migrations
alembic upgrade head

# Change to the backend directory to run the application
cd /app/backend

# Start the main application
exec uvicorn main:app --host 0.0.0.0 --port ${PORT:-8000}