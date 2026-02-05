#!/usr/bin/env python3
import os
import sys
import subprocess
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def run_migrations():
    """Run alembic migrations from the current directory (backend)"""
    logger.info("Running database migrations...")
    
    # Run alembic upgrade in the current directory (already in backend)
    result = subprocess.run([
        'alembic', 'upgrade', 'head'
    ], 
    env=os.environ,
    capture_output=True,
    text=True
    )
    
    if result.returncode != 0:
        logger.error(f"Alembic migration failed: {result.stderr}")
        raise Exception(f"Alembic migration failed: {result.stderr}")
    
    logger.info("Database migrations completed successfully")

def start_application():
    """Start the main application"""
    logger.info("Starting application...")
    
    # Set default database URL if not provided
    if 'DATABASE_URL' not in os.environ:
        os.environ['DATABASE_URL'] = 'sqlite:///./todo_chatbot.db'
    
    # Add backend to Python path
    sys.path.insert(0, '/app/backend')
    
    # Import and run the start_server functionality
    import start_server
    start_server.main()

if __name__ == "__main__":
    logger.info("Application starting...")
    
    # Set database URL from environment or default
    database_url = os.environ.get('DATABASE_URL', 'sqlite:///./todo_chatbot.db')
    os.environ['DATABASE_URL'] = database_url
    
    # Run migrations
    run_migrations()
    
    # Start the application
    start_application()