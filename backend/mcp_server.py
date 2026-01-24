#!/usr/bin/env python3
"""
Todo AI Chatbot MCP Server
Implements the Model Context Protocol to expose todo management tools to AI agents
"""

import asyncio
import json
import logging
import sys
from typing import Dict, Any, List
from contextlib import asynccontextmanager

from fastapi import FastAPI, WebSocket
from sqlmodel import Session, select
from models import Task, engine
from pydantic import BaseModel
from datetime import datetime


# Define the tool schemas
class ToolResult(BaseModel):
    """Represents the result of a tool execution"""
    tool_name: str
    output: Any
    is_error: bool = False


class AddTaskParams(BaseModel):
    user_id: str  # Changed back to str to match DB column type
    title: str
    description: str = None


class ListTasksParams(BaseModel):
    user_id: str  # Changed back to str to match DB column type
    status: str = "all"  # "all", "pending", "completed"


class CompleteTaskParams(BaseModel):
    user_id: str  # Changed back to str to match DB column type
    task_id: int


class DeleteTaskParams(BaseModel):
    user_id: str  # Changed back to str to match DB column type
    task_id: int


class UpdateTaskParams(BaseModel):
    user_id: str  # Changed back to str to match DB column type
    task_id: int
    title: str = None
    description: str = None


class MCPServer:
    def __init__(self):
        self.tools = {
            "add_task": self.add_task,
            "list_tasks": self.list_tasks,
            "complete_task": self.complete_task,
            "delete_task": self.delete_task,
            "update_task": self.update_task,
        }
        self.logger = logging.getLogger(__name__)

    async def add_task(self, params: AddTaskParams) -> Dict[str, Any]:
        """Create a new task"""
        try:
            with Session(engine) as session:
                # Convert integer user_id to string for storage in DB column
                user_id_str = str(params.user_id)
                task = Task(
                    user_id=user_id_str,  # Store as string to match DB schema
                    title=params.title,
                    description=params.description,
                    completed=False
                )
                session.add(task)
                session.commit()
                session.refresh(task)

                return {
                    "task_id": task.id,
                    "status": "created",
                    "title": task.title
                }
        except Exception as e:
            self.logger.error(f"Error adding task: {str(e)}")
            return {"error": str(e)}

    async def list_tasks(self, params: ListTasksParams) -> List[Dict[str, Any]]:
        """Retrieve tasks from the list"""
        try:
            with Session(engine) as session:
                # Convert integer user_id to string for comparison with DB column
                user_id_str = str(params.user_id)
                statement = select(Task).where(Task.user_id == user_id_str)

                if params.status == "pending":
                    statement = statement.where(Task.completed == False)
                elif params.status == "completed":
                    statement = statement.where(Task.completed == True)

                tasks = session.exec(statement).all()

                return [
                    {
                        "id": task.id,
                        "title": task.title,
                        "completed": task.completed
                    }
                    for task in tasks
                ]
        except Exception as e:
            self.logger.error(f"Error listing tasks: {str(e)}")
            return {"error": str(e)}

    async def complete_task(self, params: CompleteTaskParams) -> Dict[str, Any]:
        """Mark a task as complete"""
        try:
            with Session(engine) as session:
                # Convert integer user_id to string for comparison with DB column
                user_id_str = str(params.user_id)

                task = session.get(Task, params.task_id)

                if not task or str(task.user_id) != user_id_str:
                    return {"error": f"Task {params.task_id} not found for user {params.user_id}"}

                task.completed = True
                session.add(task)
                session.commit()
                session.refresh(task)

                return {
                    "task_id": task.id,
                    "status": "completed",
                    "title": task.title
                }
        except Exception as e:
            self.logger.error(f"Error completing task: {str(e)}")
            return {"error": str(e)}

    async def delete_task(self, params: DeleteTaskParams) -> Dict[str, Any]:
        """Remove a task from the list"""
        try:
            with Session(engine) as session:
                # Convert integer user_id to string for comparison with DB column
                user_id_str = str(params.user_id)

                task = session.get(Task, params.task_id)

                if not task or str(task.user_id) != user_id_str:
                    return {"error": f"Task {params.task_id} not found for user {params.user_id}"}

                session.delete(task)
                session.commit()

                return {
                    "task_id": params.task_id,
                    "status": "deleted",
                    "title": task.title
                }
        except Exception as e:
            self.logger.error(f"Error deleting task: {str(e)}")
            return {"error": str(e)}

    async def update_task(self, params: UpdateTaskParams) -> Dict[str, Any]:
        """Modify task title or description"""
        try:
            with Session(engine) as session:
                # Convert integer user_id to string for comparison with DB column
                user_id_str = str(params.user_id)

                task = session.get(Task, params.task_id)

                if not task or str(task.user_id) != user_id_str:
                    return {"error": f"Task {params.task_id} not found for user {params.user_id}"}

                if params.title is not None:
                    task.title = params.title
                if params.description is not None:
                    task.description = params.description

                task.updated_at = datetime.utcnow()
                session.add(task)
                session.commit()
                session.refresh(task)

                return {
                    "task_id": task.id,
                    "status": "updated",
                    "title": task.title
                }
        except Exception as e:
            self.logger.error(f"Error updating task: {str(e)}")
            return {"error": str(e)}

    async def execute_tool(self, tool_name: str, params: Dict[str, Any]) -> ToolResult:
        """Execute a tool with the given parameters"""
        if tool_name not in self.tools:
            return ToolResult(tool_name=tool_name, output={"error": f"Tool {tool_name} not found"}, is_error=True)

        try:
            # Get the tool function
            tool_func = self.tools[tool_name]
            
            # Create the appropriate parameter model
            param_model = {
                "add_task": AddTaskParams,
                "list_tasks": ListTasksParams,
                "complete_task": CompleteTaskParams,
                "delete_task": DeleteTaskParams,
                "update_task": UpdateTaskParams,
            }.get(tool_name)
            
            if param_model:
                validated_params = param_model(**params)
                result = await tool_func(validated_params)
            else:
                result = await tool_func(params)
                
            return ToolResult(tool_name=tool_name, output=result, is_error=False)
        except Exception as e:
            self.logger.error(f"Error executing tool {tool_name}: {str(e)}")
            return ToolResult(tool_name=tool_name, output={"error": str(e)}, is_error=True)


# Initialize the MCP server
mcp_server = MCPServer()

# Create FastAPI app with lifespan to manage the MCP server
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    yield
    # Shutdown


app = FastAPI(
    title="Todo AI Chatbot MCP Server",
    description="Model Context Protocol server for todo management tools",
    version="1.0.0",
    lifespan=lifespan
)


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            # Receive tool execution request
            data = await websocket.receive_text()
            request = json.loads(data)
            
            # Validate request structure
            if "method" not in request or "params" not in request:
                error_response = {
                    "id": request.get("id"),
                    "result": None,
                    "error": {"message": "Invalid request format"}
                }
                await websocket.send_text(json.dumps(error_response))
                continue
                
            method = request["method"]
            params = request["params"]
            
            # Execute the tool
            result = await mcp_server.execute_tool(method, params)
            
            # Send response
            response = {
                "id": request.get("id"),
                "result": result.output,
                "error": {"message": str(result.output)} if result.is_error else None
            }
            await websocket.send_text(json.dumps(response))
    except Exception as e:
        logging.error(f"WebSocket error: {str(e)}")
    finally:
        await websocket.close()


@app.get("/")
async def root():
    return {"message": "Todo AI Chatbot MCP Server is running"}


@app.get("/tools")
async def get_tools():
    """Return the list of available tools"""
    return {"tools": list(mcp_server.tools.keys())}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=3000)