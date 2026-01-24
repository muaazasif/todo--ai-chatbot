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

# Copy the startup script
COPY start_server.py .
COPY start_app.sh .
RUN chmod +x start_app.sh

# Run the application - the port will be set by Railway
CMD ["sh", "-c", "alembic upgrade head && exec sh start_app.sh"]