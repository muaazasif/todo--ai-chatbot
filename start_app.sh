#!/bin/sh

# Set database URL
export DATABASE_URL=${DATABASE_URL:-"sqlite:///./todo_chatbot.db"}

# Run the migrations from the backend directory
cd /app/backend && alembic upgrade head

# Start the main application using start_server.py
cd /app && exec python start_server.py