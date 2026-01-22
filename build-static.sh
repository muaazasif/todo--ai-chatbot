#!/bin/bash
# Build script for static hosting

echo "Building frontend for static hosting..."

# Navigate to frontend directory
cd /home/muaaz/Desktop/Governor\ Sindh\ IT/todo-ai-chatbot/frontend

# Install dependencies
npm install

# Build the application for static export
npm run build

# Create the out directory if it doesn't exist in the project root
cd ..
mkdir -p docs

# Copy the built static files to docs directory for GitHub Pages
cp -r frontend/out/* docs/ 2>/dev/null || echo "Build output may be in a different location"

echo "Build completed. Files are in the docs/ directory for GitHub Pages."