from sqlmodel import SQLModel, Field, create_engine, Session, select
from datetime import datetime
from typing import Optional
import os
from pydantic_settings import BaseSettings
from auth import User, get_password_hash

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

def test_user_creation():
    # Create tables
    SQLModel.metadata.create_all(bind=engine)
    
    # Create a test user
    with Session(engine) as session:
        # Check if test user already exists
        existing_user = session.exec(select(User).where(User.username == "testuser")).first()
        if existing_user:
            print("Test user already exists")
            return
            
        # Create new user
        test_user = User(
            email="test@example.com",
            username="testuser",
            hashed_password=get_password_hash("password123")
        )
        session.add(test_user)
        session.commit()
        session.refresh(test_user)
        
        print(f"Created user with ID: {test_user.id}")
        
        # Query to verify the user was created
        users = session.exec(select(User)).all()
        print(f"Total users in database: {len(users)}")
        for user in users:
            print(f"User ID: {user.id}, Username: {user.username}, Email: {user.email}")

if __name__ == "__main__":
    test_user_creation()