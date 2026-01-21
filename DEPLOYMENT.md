# Deployment Guide for Railway

This guide explains how to deploy the Todo AI Chatbot application on Railway.

## Prerequisites

- Railway account ([https://railway.app](https://railway.app))
- Railway CLI installed (`npm install -g @railway/cli`)
- GitHub account with the repository

## Quick Deploy with Railway Button

[![Deploy on Railway](https://railway.app/button.svg)](https://railway.app/new/template?template=https://github.com/muaazasif/todo--ai-chatbot)

## Manual Deployment Steps

### 1. Login to Railway

```bash
railway login
```

### 2. Create a new project

```bash
railway init
```

### 3. Link your project

```bash
railway link
```

### 4. Set environment variables

```bash
railway var set OPENAI_API_KEY=your_openai_api_key
railway var set AUTH_SECRET=your_auth_secret
railway var set SECRET_KEY=your_secret_key
```

### 5. Deploy

```bash
railway deploy
```

## Configuration

### Environment Variables

The following environment variables need to be set in Railway:

- `DATABASE_URL`: PostgreSQL database connection string (automatically provided by Railway's PostgreSQL plugin)
- `OPENAI_API_KEY`: Your OpenAI API key for AI functionality
- `GEMINI_API_KEY`: Your Google Gemini API key (alternative to OpenAI)
- `AUTH_SECRET`: Secret key for authentication (generate a random string)
- `SECRET_KEY`: Secret key for JWT tokens (generate a random string)
- `MCP_SERVER_HOST`: Host for the MCP server (default: localhost)
- `MCP_SERVER_PORT`: Port for the MCP server (default: 3000)

### Railway Configuration

The project includes a `railway.toml` file that specifies the build and deployment configuration:

```toml
[build]
builder = "heroku/buildpacks:20"

[build.args]
NODE_VERSION = "18.17.0"
PYTHON_VERSION = "3.11.5"

[deploy]
numReplicas = 1
region = "us-central1"
ephemeral = false

[env]
OPENAI_API_KEY = { description = "OpenAI API Key for AI functionality", required = true }
DATABASE_URL = { description = "Database connection string", required = true }
AUTH_SECRET = { description = "Secret key for authentication", required = true }
SECRET_KEY = { description = "Secret key for JWT tokens", required = true }
MCP_SERVER_HOST = { default = "localhost", description = "Host for the MCP server" }
MCP_SERVER_PORT = { default = "3000", description = "Port for the MCP server" }
```

## Database Setup

The application uses PostgreSQL with automatic migrations. Railway will automatically provision a PostgreSQL database when you deploy.

## MCP Server

The application includes an MCP (Model Context Protocol) server that handles AI tool operations. This service runs alongside the main backend.

## Monitoring

After deployment, you can monitor your application using Railway's dashboard:

- View logs
- Monitor resource usage
- Adjust scaling settings
- Manage environment variables

## Scaling

The application is designed to scale horizontally. You can adjust the number of replicas in the Railway dashboard based on your traffic needs.

## Troubleshooting

### Common Issues

1. **Database Connection Errors**: Ensure the `DATABASE_URL` is correctly set
2. **API Key Issues**: Verify that your OpenAI or Gemini API key is valid
3. **Authentication Problems**: Check that `AUTH_SECRET` and `SECRET_KEY` are properly set

### Logs

Check application logs in the Railway dashboard to troubleshoot issues:

```bash
railway logs
```

## Updating the Application

To update your deployed application:

1. Make changes to your code
2. Commit and push to GitHub
3. Railway will automatically redeploy the application

Or manually deploy:

```bash
railway up
```

## Support

For support with deployment, contact Railway support or open an issue in the GitHub repository.