from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
import os
from typing import Optional
from pydantic import BaseModel
from sqlmodel import SQLModel, Field, create_engine, Session, select
from contextlib import asynccontextmanager
from datetime import datetime
import uuid
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Import models
from models import Task, Conversation, Message, engine, User

# Import routes
from routes.chat import router as chat_router
from routes.auth import router as auth_router
from routes.auth_routes import router as auth_routes_router, get_current_user

# Initialize the FastAPI app
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Create tables on startup
    SQLModel.metadata.create_all(bind=engine)
    yield

app = FastAPI(
    title="Todo AI Chatbot API",
    description="An AI-powered chatbot interface for managing todos through natural language",
    version="1.0.0",
    lifespan=lifespan
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth_routes_router)  # Include the new authentication routes
app.include_router(chat_router, prefix="/api")
app.include_router(auth_router, prefix="/auth")

@app.get("/")
def read_root():
    return {"message": "Welcome to Todo AI Chatbot API"}

# Health check endpoint
@app.get("/health")
def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)