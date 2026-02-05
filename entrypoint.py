#!/usr/bin/env python3
import os
import sys
import subprocess
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def run_migrations():
    """Run alembic migrations from the backend directory"""
    logger.info("Running database migrations...")
    
    # Change to backend directory to run alembic
    backend_dir = "/app/backend"
    original_dir = os.getcwd()
    
    try:
        os.chdir(backend_dir)
        logger.info(f"Changed to directory: {os.getcwd()}")
        
        # Run alembic upgrade
        result = subprocess.run(
            ["alembic", "upgrade", "head"],
            cwd=backend_dir,
            capture_output=True,
            text=True
        )
        
        if result.returncode != 0:
            logger.error(f"Alembic migration failed: {result.stderr}")
            raise Exception(f"Alembic migration failed: {result.stderr}")
        
        logger.info("Database migrations completed successfully")
        
    finally:
        # Change back to original directory
        os.chdir(original_dir)
        logger.info(f"Changed back to directory: {os.getcwd()}")

def start_application():
    """Start the main application"""
    logger.info("Starting application...")
    
    # Set default database URL if not provided
    if 'DATABASE_URL' not in os.environ:
        os.environ['DATABASE_URL'] = 'sqlite:///./todo_chatbot.db'
    
    # Add backend to Python path
    sys.path.insert(0, '/app/backend')
    
    # Import and run the start_server functionality
    try:
        import start_server
        start_server.main()  # Assuming start_server has a main function
    except ImportError:
        # If start_server doesn't have a main function, execute it differently
        import importlib.util
        spec = importlib.util.spec_from_file_location("start_server", "/app/start_server.py")
        start_server_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(start_server_module)

if __name__ == "__main__":
    logger.info("Application starting...")
    
    # Set database URL from environment or default
    database_url = os.environ.get('DATABASE_URL', 'sqlite:///./todo_chatbot.db')
    os.environ['DATABASE_URL'] = database_url
    
    # Run migrations
    run_migrations()
    
    # Start the application
    start_application()