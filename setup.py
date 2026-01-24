from setuptools import setup, find_packages

setup(
    name="todo-ai-chatbot-backend",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[
        "fastapi==0.104.1",
        "uvicorn==0.24.0",
        "sqlmodel==0.0.16",
        "pydantic==2.5.0",
        "pydantic-settings==2.1.0",
        "asyncpg==0.29.0",
        "alembic==1.13.1",
        "python-multipart==0.0.6",
        "openai==1.3.5",
        "sse-starlette==1.6.5",
        "python-jose[cryptography]==3.3.0",
        "passlib[bcrypt]==1.7.4",
        "websockets==12.0",
        "bcrypt==4.0.1",
        "psycopg2-binary",
        "pg8000==1.29.8",
    ],
)