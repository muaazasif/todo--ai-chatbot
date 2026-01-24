# Production Dockerfile for Todo AI Chatbot Backend

FROM node:18-alpine AS frontend-builder

WORKDIR /app

# Copy frontend package files and install dependencies
COPY frontend/package*.json ./
RUN npm ci --only=production

# Copy frontend source code and build
COPY frontend/ .
RUN npm run build

# Backend stage
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Copy backend requirements and install Python dependencies
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy backend source code
COPY backend/ .

# Copy setup.py to the app directory
COPY setup.py .

# Copy built frontend from the previous stage
COPY --from=frontend-builder /app/out ./frontend/out

# Install the backend as a package
RUN pip install -e .

# Set the working directory to /app where alembic.ini is located
WORKDIR /app

# Run the application - the port will be set by Railway
CMD ["sh", "-c", "alembic upgrade head && exec python -c \"import os; import sys; sys.path.append('/app/backend'); import uvicorn; from backend.main import app; port=int(os.environ.get('PORT', 8000)); print(f'Using port: {port}'); uvicorn.run(app, host='0.0.0.0', port=port)\""]