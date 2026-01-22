# Todo AI Chatbot

An AI-powered chatbot interface for managing todos through natural language.

## Features

- Natural language task management
- AI-powered task creation and management
- User authentication and session management
- Real-time chat interface
- Task CRUD operations

## Live Demo

The application is deployed on GitHub Pages and connects to the Railway backend:
- **Frontend**: https://muaazasif.github.io/todo--ai-chatbot/
- **Backend**: https://todo-ai-chatbot-production.up.railway.app/

## Architecture

This application consists of two main components:

1. **Backend**: FastAPI server with SQLModel and PostgreSQL database (deployed on Railway)
2. **Frontend**: Next.js application with Tailwind CSS (deployed on GitHub Pages)

## Local Development

### Backend Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Set up environment variables in `.env`:
```env
DATABASE_URL=postgresql://username:password@ep-xxx.us-east-1.aws.neon.tech/neondb?sslmode=require
SECRET_KEY=your-super-secret-key-change-this-in-production
GEMINI_API_KEY=your-gemini-api-key-here
```

3. Run the backend:
```bash
cd backend
uvicorn main:app --host 0.0.0.0 --port 8000
```

### Frontend Setup

1. Install dependencies:
```bash
cd frontend
npm install
```

2. Run the development server:
```bash
npm run dev
```

## GitHub Pages Deployment

The static build is located in the `docs` folder. The application is already configured for GitHub Pages deployment with proper asset paths.

## How It Works

The frontend communicates with the backend API hosted on Railway. When users interact with the chat interface:

1. Authentication requests (login/register) are sent to `/auth/login` and `/auth/register`
2. Chat messages are sent to `/api/chat`
3. The backend processes the natural language using AI tools
4. Tasks are created, updated, or deleted in the PostgreSQL database
5. Responses are returned to the frontend for display

## Troubleshooting

If you encounter CORS issues, make sure your backend allows requests from your GitHub Pages domain.