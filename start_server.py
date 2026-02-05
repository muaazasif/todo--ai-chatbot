#!/usr/bin/env python3

import os
import sys
import subprocess
import logging

def run_migrations():
    """Run database migrations using alembic directly in Python"""
    try:
        # Import alembic modules directly to run migrations without shell commands
        import subprocess
        import sys
        
        # Add backend to Python path for alembic to find models
        sys.path.insert(0, '/app/backend')
        
        # Run migrations using Python's alembic module directly
        from alembic.config import Config
        from alembic import command
        import psycopg2
        
        # Create alembic config, pointing to the alembic.ini file
        # According to Dockerfile, alembic.ini is copied to /app directory
        alembic_cfg = Config("/app/alembic.ini")
        
        # Run the upgrade command
        command.upgrade(alembic_cfg, "head")
        print("Database migrations completed successfully")
        return True
        
    except ImportError:
        print("Alembic not available, skipping migrations")
        return True  # Don't fail if alembic isn't available
    except Exception as e:
        # Check if it's a duplicate table error - this can be safely ignored
        error_str = str(e)
        if "DuplicateTable" in error_str or "already exists" in error_str.lower():
            print("Database tables already exist, skipping migration")
            return True
        else:
            print(f"Error running migrations: {str(e)}")
            return False

def main():
    # Run database migrations first
    print("Running database migrations...")
    if not run_migrations():
        print("Failed to run migrations, exiting...")
        sys.exit(1)
    
    print("Migrations completed, starting application...")

    # Add the backend directory to Python path
    sys.path.insert(0, '/app/backend')

    # Set environment variable to help with imports
    os.environ['PYTHONPATH'] = '/app/backend'

    # Set default database URL to SQLite for local development/testing
    if 'DATABASE_URL' not in os.environ:
        os.environ['DATABASE_URL'] = 'sqlite:///./todo_chatbot.db'

    # Import and run the application directly
    import importlib.util

    # Load the main module directly from file in the backend directory
    spec = importlib.util.spec_from_file_location("main", "/app/backend/main.py")
    main_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(main_module)

    # Get the app instance
    app = main_module.app

    # Get the port from environment
    port = int(os.environ.get("PORT", 8000))
    print(f"PORT environment variable value: {os.environ.get('PORT')}")
    print(f"Using port: {port}")

    # Run the app directly using the ASGI interface
    import asyncio
    from uvicorn import Config, Server

    config = Config(app=app, host="0.0.0.0", port=port, log_level="info")
    server = Server(config=config)

    # Run the server
    import signal
    import uvicorn

    # Just run the server without using uvicorn's run function to avoid reload issues
    if os.name == "nt":  # Windows
        signal.signal(signal.SIGINT, lambda s, f: sys.exit(0))
        signal.signal(signal.SIGTERM, lambda s, f: sys.exit(0))
    else:  # Unix-like systems
        signal.signal(signal.SIGINT, lambda s, f: sys.exit(0))
        signal.signal(signal.SIGTERM, lambda s, f: sys.exit(0))

    uvicorn.run(app, host="0.0.0.0", port=port, lifespan="on", reload=False)

if __name__ == "__main__":
    main()