from sqlmodel import SQLModel, Field, create_engine, Session, select
from datetime import datetime
from typing import Optional
import os
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    database_url: str = os.getenv("DATABASE_URL", "sqlite:///./todo_chatbot.db")


settings = Settings()
# Use SQLite for local development, PostgreSQL for production
if settings.database_url.startswith("sqlite"):
    engine = create_engine(settings.database_url, echo=True)
else:
    # For PostgreSQL, use connect_args to handle SSL
    engine = create_engine(settings.database_url, echo=True, connect_args={
        "sslmode": "require"
    })


# Simple test to check database connection
def test_connection():
    try:
        # Import User model from auth module
        from auth import User
        
        # Create tables
        SQLModel.metadata.create_all(bind=engine)
        
        # Test connection by querying users
        with Session(engine) as session:
            users = session.exec(select(User)).all()
            print(f"Connected successfully! Found {len(users)} users in the database.")
            return True
    except Exception as e:
        print(f"Connection failed: {str(e)}")
        return False

if __name__ == "__main__":
    test_connection()