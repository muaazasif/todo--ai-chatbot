# backend/test_app.py
"""
Test script for Todo AI Chatbot
Validates core functionality without requiring external services
"""

import pytest
from fastapi.testclient import TestClient
from main import app
from sqlmodel import create_engine, SQLModel, Session
from models import Task, Conversation, Message
from unittest.mock import patch, AsyncMock


@pytest.fixture
def client():
    """Create a test client for the FastAPI app"""
    with TestClient(app) as test_client:
        yield test_client


@pytest.fixture
def mock_db_session():
    """Create a mock database session"""
    engine = create_engine("sqlite:///./test.db", echo=True)
    SQLModel.metadata.create_all(bind=engine)
    with Session(engine) as session:
        yield session


def test_health_check(client):
    """Test the health check endpoint"""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}


def test_root_endpoint(client):
    """Test the root endpoint"""
    response = client.get("/")
    assert response.status_code == 200
    assert "message" in response.json()


@patch('agents.run_agent', new_callable=AsyncMock)
def test_chat_endpoint(mock_run_agent, client):
    """Test the chat endpoint with mocked agent response"""
    # Mock the agent response
    mock_run_agent.return_value = {
        "response": "Task 'Buy groceries' has been added to your list.",
        "tool_calls": [{"name": "add_task", "arguments": {"title": "Buy groceries"}}]
    }
    
    # Test data
    test_data = {
        "user_id": "test_user_123",
        "message": "Add a task to buy groceries"
    }
    
    # Make request to chat endpoint
    response = client.post("/api/test_user_123/chat", json=test_data)
    
    # Validate response
    assert response.status_code == 200
    data = response.json()
    assert "conversation_id" in data
    assert "response" in data
    assert "tool_calls" in data
    assert isinstance(data["tool_calls"], list)


def test_models_creation():
    """Test that database models can be instantiated"""
    # Test Task model
    task = Task(
        user_id="test_user",
        title="Test task",
        description="Test description",
        completed=False
    )
    assert task.user_id == "test_user"
    assert task.title == "Test task"
    
    # Test Conversation model
    conversation = Conversation(user_id="test_user")
    assert conversation.user_id == "test_user"
    
    # Test Message model
    message = Message(
        user_id="test_user",
        conversation_id=1,
        role="user",
        content="Test message"
    )
    assert message.user_id == "test_user"
    assert message.role == "user"
    assert message.content == "Test message"


@patch('agents.run_agent', new_callable=AsyncMock)
def test_conversation_flow(mock_run_agent, client):
    """Test a complete conversation flow"""
    # Mock responses for different agent calls
    mock_responses = [
        {
            "response": "Task 'Buy groceries' has been added to your list.",
            "tool_calls": [{"name": "add_task", "arguments": {"title": "Buy groceries"}}]
        },
        {
            "response": "Here are your pending tasks: Buy groceries.",
            "tool_calls": [{"name": "list_tasks", "arguments": {"status": "pending"}}]
        },
        {
            "response": "Task 'Buy groceries' has been marked as completed.",
            "tool_calls": [{"name": "complete_task", "arguments": {"task_id": 1}}]
        }
    ]
    
    call_count = 0
    
    async def mock_side_effect(*args, **kwargs):
        nonlocal call_count
        result = mock_responses[call_count]
        call_count = min(call_count + 1, len(mock_responses) - 1)
        return result
    
    mock_run_agent.side_effect = mock_side_effect
    
    # Step 1: Add a task
    response1 = client.post("/api/test_user_123/chat", json={
        "user_id": "test_user_123",
        "message": "Add a task to buy groceries"
    })
    assert response1.status_code == 200
    data1 = response1.json()
    conversation_id = data1["conversation_id"]
    
    # Step 2: List pending tasks
    response2 = client.post("/api/test_user_123/chat", json={
        "user_id": "test_user_123",
        "conversation_id": conversation_id,
        "message": "What's pending?"
    })
    assert response2.status_code == 200
    
    # Step 3: Complete the task
    response3 = client.post("/api/test_user_123/chat", json={
        "user_id": "test_user_123",
        "conversation_id": conversation_id,
        "message": "Mark the grocery task as complete"
    })
    assert response3.status_code == 200


if __name__ == "__main__":
    pytest.main([__file__])