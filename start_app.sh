#!/bin/bash

# Set database URL to SQLite for local development/testing
export DATABASE_URL="sqlite:///./todo_chatbot.db"

# Change to the backend directory where alembic.ini is located for migrations
cd "/home/muaaz/Desktop/Governor Sindh IT/todo-ai-chatbot/backend"

# Run the migrations
alembic upgrade head

# Start the main application
exec uvicorn main:app --host 0.0.0.0 --port ${PORT:-8000}