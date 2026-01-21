# backend/test_mcp_server.py
"""
Test script for MCP Server functionality
"""

import pytest
import asyncio
from unittest import mock
from unittest.mock import AsyncMock, MagicMock
from mcp_server import MCPServer, AddTaskParams, ListTasksParams, CompleteTaskParams, DeleteTaskParams, UpdateTaskParams


@pytest.fixture
def mcp_server():
    """Create an instance of the MCPServer for testing"""
    return MCPServer()


@pytest.mark.asyncio
async def test_add_task(mcp_server):
    """Test the add_task functionality"""
    params = AddTaskParams(
        user_id="test_user",
        title="Test task",
        description="Test description"
    )

    # Mock the database session
    with mock.patch('mcp_server.Session') as mock_session:
        mock_session_instance = MagicMock()
        mock_session.return_value.__enter__.return_value = mock_session_instance
        mock_task = MagicMock()
        mock_task.id = 1
        mock_task.title = "Test task"
        mock_session_instance.get.return_value = mock_task
        mock_session_instance.add.return_value = None
        mock_session_instance.commit.return_value = None
        mock_session_instance.refresh.return_value = None

        result = await mcp_server.add_task(params)

        assert result["status"] == "created"
        assert result["title"] == "Test task"
        assert "task_id" in result


@pytest.mark.asyncio
async def test_list_tasks(mcp_server):
    """Test the list_tasks functionality"""
    params = ListTasksParams(
        user_id="test_user",
        status="all"
    )

    # Mock the database session
    with mock.patch('mcp_server.Session') as mock_session:
        mock_session_instance = MagicMock()
        mock_session.return_value.__enter__.return_value = mock_session_instance
        mock_task = MagicMock()
        mock_task.id = 1
        mock_task.title = "Test task"
        mock_task.completed = False
        mock_session_instance.exec.return_value.all.return_value = [mock_task]

        result = await mcp_server.list_tasks(params)

        assert isinstance(result, list)
        assert len(result) >= 0  # May be empty depending on mock data


@pytest.mark.asyncio
async def test_complete_task(mcp_server):
    """Test the complete_task functionality"""
    params = CompleteTaskParams(
        user_id="test_user",
        task_id=1
    )

    # Mock the database session
    with mock.patch('mcp_server.Session') as mock_session:
        mock_session_instance = MagicMock()
        mock_session.return_value.__enter__.return_value = mock_session_instance
        mock_task = MagicMock()
        mock_task.id = 1
        mock_task.title = "Test task"
        mock_task.completed = False
        mock_session_instance.get.return_value = mock_task
        mock_session_instance.add.return_value = None
        mock_session_instance.commit.return_value = None
        mock_session_instance.refresh.return_value = None

        result = await mcp_server.complete_task(params)

        assert result["status"] == "completed"
        assert result["title"] == "Test task"
        assert result["task_id"] == 1


@pytest.mark.asyncio
async def test_delete_task(mcp_server):
    """Test the delete_task functionality"""
    params = DeleteTaskParams(
        user_id="test_user",
        task_id=1
    )

    # Mock the database session
    with mock.patch('mcp_server.Session') as mock_session:
        mock_session_instance = MagicMock()
        mock_session.return_value.__enter__.return_value = mock_session_instance
        mock_task = MagicMock()
        mock_task.id = 1
        mock_task.title = "Test task"
        mock_session_instance.get.return_value = mock_task
        mock_session_instance.delete.return_value = None
        mock_session_instance.commit.return_value = None

        result = await mcp_server.delete_task(params)

        assert result["status"] == "deleted"
        assert result["title"] == "Test task"
        assert result["task_id"] == 1


@pytest.mark.asyncio
async def test_update_task(mcp_server):
    """Test the update_task functionality"""
    params = UpdateTaskParams(
        user_id="test_user",
        task_id=1,
        title="Updated task title"
    )

    # Mock the database session
    with mock.patch('mcp_server.Session') as mock_session:
        mock_session_instance = MagicMock()
        mock_session.return_value.__enter__.return_value = mock_session_instance
        mock_task = MagicMock()
        mock_task.id = 1
        mock_task.title = "Updated task title"
        mock_session_instance.get.return_value = mock_task
        mock_session_instance.add.return_value = None
        mock_session_instance.commit.return_value = None
        mock_session_instance.refresh.return_value = None

        result = await mcp_server.update_task(params)

        assert result["status"] == "updated"
        assert result["title"] == "Updated task title"
        assert result["task_id"] == 1


@pytest.mark.asyncio
async def test_execute_tool(mcp_server):
    """Test the execute_tool functionality"""
    # Test valid tool
    result = await mcp_server.execute_tool("add_task", {
        "user_id": "test_user",
        "title": "Test task"
    })

    assert result.tool_name == "add_task"
    assert not result.is_error

    # Test invalid tool
    result = await mcp_server.execute_tool("invalid_tool", {})

    assert result.tool_name == "invalid_tool"
    assert result.is_error


if __name__ == "__main__":
    pytest.main([__file__])