from sqlmodel import SQLModel, Field, create_engine
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


# Import User model from auth module
from auth import User


class Task(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: str  # String to match database schema
    title: str
    description: Optional[str] = None
    completed: bool = False
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)


class Conversation(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: str  # String to match database schema
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)


class Message(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: str  # String to match database schema
    conversation_id: int
    role: str  # "user" or "assistant"
    content: str
    created_at: datetime = Field(default_factory=datetime.utcnow)