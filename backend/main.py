from fastapi import FastAPI, HTTPException, Depends, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, FileResponse
import os
import logging
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

# Serve frontend files
frontend_dir = "/app/frontend/out"  # Absolute path in Docker container

logging.info(f"Looking for frontend files at: {frontend_dir}")
logging.info(f"Frontend dir exists: {os.path.exists(frontend_dir)}")

if os.path.exists(frontend_dir):
    app.mount("/static", StaticFiles(directory=os.path.join(frontend_dir, "_next", "static")), name="static")

    @app.get("/", response_class=HTMLResponse)
    async def serve_frontend(request: Request):
        frontend_file = os.path.join(frontend_dir, "index.html")
        logging.info(f"Serving index.html from: {frontend_file}")
        logging.info(f"Index file exists: {os.path.exists(frontend_file)}")
        if os.path.exists(frontend_file):
            with open(frontend_file, "r") as f:
                content = f.read()
            return HTMLResponse(content=content)
        else:
            return {"message": "Welcome to Todo AI Chatbot API - Frontend index.html not found"}

    @app.get("/{full_path:path}", response_class=HTMLResponse)
    async def serve_frontend_pages(full_path: str, request: Request):
        # Try to serve the requested file, fallback to index.html for SPA
        requested_file = os.path.join(frontend_dir, full_path)

        # If the requested file exists and is not a directory, serve it
        if os.path.exists(requested_file) and not os.path.isdir(requested_file):
            if requested_file.endswith('.html'):
                with open(requested_file, "r") as f:
                    content = f.read()
                return HTMLResponse(content=content)
            elif requested_file.endswith(('.js', '.css', '.json', '.png', '.jpg', '.jpeg', '.gif', '.svg', '.ico')):
                return FileResponse(requested_file)

        # For SPA, serve index.html for all other routes
        index_file = os.path.join(frontend_dir, "index.html")
        if os.path.exists(index_file):
            with open(index_file, "r") as f:
                content = f.read()
            return HTMLResponse(content=content)
        else:
            return {"message": "Welcome to Todo AI Chatbot API - Frontend index.html not found"}
else:
    @app.get("/")
    def read_root():
        return {"message": "Welcome to Todo AI Chatbot API - Frontend directory not found"}

# Health check endpoint
@app.get("/health")
def health_check():
    return {"status": "healthy"}

# This is the important part - make sure the app runs on the correct port
if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    logging.info(f"Starting server on port {port}")
    uvicorn.run(app, host="0.0.0.0", port=port)