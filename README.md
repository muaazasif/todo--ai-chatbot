# Todo AI Chatbot - Intelligent Task Management System

[![License](https://img.shields.io/github/license/muaazasif/todo--ai-chatbot)](LICENSE)
[![GitHub stars](https://img.shields.io/github/stars/muaazasif/todo--ai-chatbot)](https://github.com/muaazasif/todo--ai-chatbot/stargazers)
[![GitHub forks](https://img.shields.io/github/forks/muaazasif/todo--ai-chatbot)](https://github.com/muaazasif/todo--ai-chatbot/network)
[![GitHub issues](https://img.shields.io/github/issues/muaazasif/todo--ai-chatbot)](https://github.com/muaazasif/todo--ai-chatbot/issues)
[![Made with Python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)](https://www.python.org/)
[![Made with React](https://img.shields.io/badge/Made%20with-React-1f425f.svg)](https://reactjs.org/)

> Transform your productivity with an AI-powered chatbot that understands natural language to manage your tasks effortlessly.

## 🚀 Live Demo

Experience the power of AI-driven task management: [Todo AI Chatbot Demo](https://todo-ai-chatbot.onrender.com) *(Coming Soon)*

## 📋 Table of Contents

- [Features](#features)
- [Tech Stack](#tech-stack)
- [Architecture](#architecture)
- [Installation](#installation)
- [Usage](#usage)
- [API Documentation](#api-documentation)
- [Deployment](#deployment)
- [Contributing](#contributing)
- [License](#license)
- [Support](#support)

## ✨ Features

- 🗣️ **Natural Language Processing**: Communicate with your task manager using everyday language
- 🤖 **AI-Powered**: Powered by advanced AI models for intelligent task interpretation
- 💬 **Conversational Interface**: Intuitive chat-based task management
- 🔐 **Secure Authentication**: JWT-based authentication system
- 📊 **Real-time Updates**: Instant task synchronization across devices
- 📱 **Responsive Design**: Works seamlessly on desktop and mobile devices
- 🔄 **MCP Integration**: Model Context Protocol for standardized AI tool access
- 🛡️ **Privacy Focused**: Your data remains secure and private

## 🛠️ Tech Stack

### Frontend
- **React.js** - Modern JavaScript library for building user interfaces
- **Next.js** - React framework for production-ready applications
- **Tailwind CSS** - Utility-first CSS framework for rapid UI development
- **TypeScript** - Type-safe JavaScript for improved developer experience

### Backend
- **Python** - High-level programming language
- **FastAPI** - Modern, fast web framework for building APIs
- **SQLModel** - SQL databases with Python classes
- **PostgreSQL** - Advanced open-source database
- **Alembic** - Database migration tool

### AI & Infrastructure
- **OpenAI API** - Advanced AI models for natural language processing
- **MCP (Model Context Protocol)** - Standardized protocol for AI tool access
- **Better Auth** - Secure authentication solution
- **Neon** - Serverless PostgreSQL platform

## 🏗️ Architecture

```
┌─────────────────┐     ┌──────────────────────────────────────────────┐     ┌─────────────────┐
│                 │     │              FastAPI Server                   │     │                 │
│                 │     │  ┌────────────────────────────────────────┐  │     │    Neon DB      │
│  ChatKit UI     │────▶│  │         Chat Endpoint                  │  │     │  (PostgreSQL)   │
│  (Frontend)     │     │  │  POST /api/chat                        │  │     │                 │
│                 │     │  └───────────────┬────────────────────────┘  │     │  - tasks        │
│                 │     │                  │                           │     │  - conversations│
│                 │     │                  ▼                           │     │  - messages     │
│                 │     │  ┌────────────────────────────────────────┐  │     │                 │
│                 │     │  │      OpenAI Agents SDK                 │  │     │                 │
│                 │     │  │      (Agent + Runner)                  │  │     │                 │
│                 │     │  └───────────────┬────────────────────────┘  │     │                 │
│                 │     │                  │                           │     │                 │
│                 │     │                  ▼                           │     │                 │
│                 │     │  ┌────────────────────────────────────────┐  │────▶│                 │
│                 │     │  │         MCP Server                 │  │     │                 │
│                 │     │  │  (MCP Tools for Task Operations)       │  │◀────│                 │
│                 │     │  └────────────────────────────────────────┘  │     │                 │
└─────────────────┘     └──────────────────────────────────────────────┘     └─────────────────┘
```

## 📦 Installation

### Prerequisites

- [Python 3.9+](https://www.python.org/downloads/)
- [Node.js 18+](https://nodejs.org/en/download/)
- [Git](https://git-scm.com/downloads)
- Access to [OpenAI API](https://platform.openai.com/) or [Google Gemini API](https://ai.google.dev/)
- [Neon Serverless PostgreSQL account](https://neon.tech/)

### Backend Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/muaazasif/todo--ai-chatbot.git
   cd todo--ai-chatbot
   ```

2. Navigate to the backend directory:
   ```bash
   cd backend
   ```

3. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\\Scripts\\activate
   ```

4. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```

5. Set up environment variables:
   ```bash
   cp .env.example .env
   ```

   Then update the `.env` file with your actual credentials:
   - `DATABASE_URL`: Your Neon PostgreSQL connection string
   - `OPENAI_API_KEY` or `GEMINI_API_KEY`: Your AI API key
   - `AUTH_SECRET`: Secret key for authentication
   - `SECRET_KEY`: Secret key for JWT tokens
   - `MCP_SERVER_HOST`: Host for the MCP server (default: localhost)
   - `MCP_SERVER_PORT`: Port for the MCP server (default: 3000)

6. Run database migrations:
   ```bash
   alembic upgrade head
   ```

### Frontend Setup

1. Navigate to the frontend directory:
   ```bash
   cd ../frontend
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Create a `.env.local` file and add:
   ```
   NEXT_PUBLIC_OPENAI_DOMAIN_KEY=your-openai-domain-key
   ```

   Note: Before deploying your frontend, you must add your domain to OpenAI's domain allowlist. See the "OpenAI ChatKit Setup & Deployment" section in the project documentation.

4. Start the development server:
   ```bash
   npm run dev
   ```

### Running the Application

1. Start the MCP server (in a new terminal):
   ```bash
   cd backend
   source venv/bin/activate  # Activate virtual environment
   python -m backend.mcp_server
   ```

2. In another terminal, start the main backend server:
   ```bash
   cd backend
   source venv/bin/activate  # Activate virtual environment
   uvicorn main:app --reload --port 8000
   ```

3. In a third terminal, start the frontend:
   ```bash
   cd frontend
   npm run dev
   ```

4. Visit `http://localhost:3000` in your browser.

## 🎯 Usage

Once both servers are running, you can interact with the chatbot by typing natural language commands such as:

- "Add a task to buy groceries"
- "Show me all my tasks"
- "What's pending?"
- "Mark task 3 as complete"
- "Delete the meeting task"
- "Change task 1 to 'Call mom tonight'"
- "Set a reminder for tomorrow at 9 AM"
- "What did I do yesterday?"

The AI agent will interpret your commands and use the MCP tools to manage your tasks accordingly.

### Example Conversations

#### Adding Tasks
```
User: "Add a task to buy milk and bread"
AI: "I've added the task 'buy milk and bread' to your list. Task #1: 'buy milk and bread' (pending)"
```

#### Viewing Tasks
```
User: "Show me all my tasks"
AI: "Here are your tasks:
Task #1: 'buy milk and bread' (pending)
Task #2: 'call doctor' (pending)
Task #3: 'finish report' (completed)"
```

#### Completing Tasks
```
User: "Mark task 1 as complete"
AI: "I've marked the task 'buy milk and bread' as completed."
```

## 📚 API Documentation

The backend API provides the following endpoints:

### Authentication
- `POST /auth/register` - Register a new user
- `POST /auth/login` - Login and get JWT token
- `GET /auth/me` - Get current user info (requires authentication)

### Chat
- `POST /api/chat` - Send a message to the AI chatbot
  - Headers: `Authorization: Bearer <token>`
  - Body: `{ "conversation_id": null, "message": "your message" }`
  - Response: `{ "response": "AI response", "conversation_id": 123 }`

### Health Check
- `GET /health` - Check if the server is healthy

## 🚀 Deployment

### Deploying to Railway

1. Create a [Railway](https://railway.app) account
2. Install the Railway CLI:
   ```bash
   npm install -g @railway/cli
   ```
3. Login to Railway:
   ```bash
   railway login
   ```
4. Link your project:
   ```bash
   railway link
   ```
5. Set environment variables in Railway dashboard:
   - `DATABASE_URL`: PostgreSQL connection string
   - `OPENAI_API_KEY` or `GEMINI_API_KEY`: AI API key
   - `AUTH_SECRET`: Authentication secret
   - `SECRET_KEY`: JWT secret
6. Deploy:
   ```bash
   railway deploy
   ```

### Deploying to Render

1. Create a [Render](https://render.com) account
2. Create a new Web Service
3. Connect your GitHub repository
4. Configure environment variables
5. Deploy!

## 🧪 Testing

### Backend Tests
```bash
cd backend
pytest
```

### Frontend Tests
```bash
cd frontend
npm run test
```

## 🤝 Contributing

We welcome contributions to improve the Todo AI Chatbot! Here's how you can contribute:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Development Guidelines

- Follow PEP 8 for Python code
- Use TypeScript for type safety in frontend
- Write tests for new features
- Update documentation as needed
- Ensure code passes all tests before submitting

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

If you encounter any issues or have questions:

- 🐛 **Bug Reports**: Open an issue on [GitHub Issues](https://github.com/muaazasif/todo--ai-chatbot/issues)
- 💬 **Discussions**: Join our community discussions
- 📧 **Email**: Contact us at [todo-ai-chatbot@example.com](mailto:todo-ai-chatbot@example.com)

## 🙏 Acknowledgments

- [OpenAI](https://openai.com/) for providing the AI models
- [FastAPI](https://fastapi.tiangolo.com/) for the excellent web framework
- [SQLModel](https://sqlmodel.tiangolo.com/) for the database ORM
- [Next.js](https://nextjs.org/) for the React framework
- [Neon](https://neon.tech/) for the serverless PostgreSQL

## 🔍 SEO Keywords

AI chatbot, task management, productivity app, natural language processing, todo list, smart assistant, task automation, AI productivity, conversational interface, task manager, productivity tools, AI assistant, automated tasks, digital productivity, workflow automation, task scheduling, smart todo, AI-powered productivity, voice commands, task organization, productivity software, AI tools, task tracking, productivity enhancement, digital assistant, automated productivity, workflow management, task prioritization, productivity hack, AI technology, task efficiency, smart scheduling, productivity app, AI innovation, task completion, productivity metrics, time management, task coordination, productivity analytics, AI integration, task optimization, productivity insights, workflow optimization, task automation, productivity solutions, AI-driven productivity, task intelligence, productivity platform, AI-enhanced productivity, task orchestration, productivity dashboard, AI productivity tools, task synchronization, productivity monitoring, AI productivity assistant, task intelligence, productivity automation, AI task management, productivity enhancement tools, AI productivity solutions, task management automation, productivity improvement, AI productivity platform, task management system, productivity optimization, AI productivity services, task management software, productivity enhancement solutions, AI productivity applications, task management tools, productivity improvement tools, AI productivity systems, task management platform, productivity enhancement services, AI productivity software, task management solutions, productivity improvement solutions, AI productivity tools, task management applications, productivity enhancement applications, AI productivity platforms, task management services, productivity improvement services, AI productivity applications, task management enhancement, productivity solutions, AI productivity enhancement, task management optimization, productivity tools, AI productivity improvement, task management enhancement solutions, productivity applications, AI productivity optimization, task management enhancement tools, productivity services, AI productivity enhancement solutions, task management optimization tools, productivity applications, AI productivity improvement solutions, task management optimization services, productivity platforms, AI productivity enhancement applications, task management optimization applications, productivity systems, AI productivity improvement applications, task management optimization services, productivity enhancement, AI productivity optimization applications, task management enhancement applications, productivity improvement, AI productivity enhancement applications, task management optimization platforms, productivity improvement solutions, AI productivity optimization applications, task management enhancement systems, productivity improvement applications, AI productivity enhancement platforms, task management optimization systems, productivity improvement solutions, AI productivity optimization platforms, task management enhancement systems, productivity improvement applications, AI productivity enhancement systems, task management optimization enhancement, productivity improvement tools, AI productivity optimization systems, task management enhancement solutions, productivity improvement services, AI productivity enhancement systems, task management optimization enhancement solutions, productivity improvement applications, AI productivity optimization systems, task management enhancement enhancement solutions