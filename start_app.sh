#!/bin/sh

# Set database URL
export DATABASE_URL=${DATABASE_URL:-"sqlite:///./todo_chatbot.db"}

# Start the main application using start_server.py
exec python /app/start_server.py