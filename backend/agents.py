import asyncio
import json
import websockets
import os

# Global counter for request IDs
request_id_counter = 0


# Instead of using WebSocket communication, let's directly import and call the MCP server functions
from mcp_server import MCPServer

# Create a single instance of the MCP server
mcp_server_instance = MCPServer()

async def send_mcp_request(method: str, params: dict) -> dict:
    """
    Send a request to the MCP server by directly calling the function
    """
    try:
        # Map method names to the corresponding functions in the MCP server
        if method == "add_task":
            from mcp_server import AddTaskParams
            validated_params = AddTaskParams(**params)
            result = await mcp_server_instance.add_task(validated_params)
            return result
        elif method == "list_tasks":
            from mcp_server import ListTasksParams
            validated_params = ListTasksParams(**params)
            result = await mcp_server_instance.list_tasks(validated_params)
            return result
        elif method == "complete_task":
            from mcp_server import CompleteTaskParams
            validated_params = CompleteTaskParams(**params)
            result = await mcp_server_instance.complete_task(validated_params)
            return result
        elif method == "delete_task":
            from mcp_server import DeleteTaskParams
            validated_params = DeleteTaskParams(**params)
            result = await mcp_server_instance.delete_task(validated_params)
            return result
        elif method == "update_task":
            from mcp_server import UpdateTaskParams
            validated_params = UpdateTaskParams(**params)
            result = await mcp_server_instance.update_task(validated_params)
            return result
        else:
            return {"error": f"Unknown method: {method}"}
    except Exception as e:
        print(f"Error calling MCP server function: {repr(e)}")
        return {"error": repr(e)}


async def run_agent(user_id: str, messages: list):
    """
    Run the agent with MCP tools to process user messages
    """
    # Check if GEMINI_API_KEY is set
    api_key = os.getenv("GEMINI_API_KEY")

    # For now, we'll use a simple rule-based approach to simulate the AI
    # In a real implementation with a working Gemini API, we would use the code below
    last_message = messages[-1]['content'].lower() if messages else ""

    # Simple rule-based processing to simulate AI behavior
    if "add" in last_message or "create" in last_message or "new" in last_message:
        # Extract task title from the message
        import re
        # Look for various patterns like "add task to go to school", "create a task i am going to school", etc.
        match = None
        # Pattern 1: "add task to ..." or "add task ..."
        match = re.search(r'add\s+task\s+(?:to\s+)?(.+?)(?:\.|$)', last_message)
        if not match:
            # Pattern 2: "add to ..." or "create to ..." or "create ..."
            match = re.search(r'(?:add|create)\s+(?:task\s+)?(?:to\s+)?(.+?)(?:\.|$)', last_message)
        if not match:
            # Pattern 3: "i am going to school" or similar
            match = re.search(r'(?:add|create|new)\s+(?:task\s+)?(.+?)(?:\.|$)', last_message)

        task_title = match.group(1).strip() if match else last_message.replace("add", "").replace("create", "").replace("task", "").strip()

        # If the extracted title is too short or generic, use the whole meaningful part
        if len(task_title) < 2:
            task_title = last_message.replace("add", "").replace("create", "").replace("task", "").replace("please", "").strip()

        # Call add_task MCP tool
        result = await send_mcp_request("add_task", {
            "user_id": user_id,
            "title": task_title
        })

        if "error" in result:
            return {
                "response": f"Sorry, I encountered an error: {result['error']}",
                "tool_calls": []
            }
        else:
            return {
                "response": f"I've added the task '{result.get('title', task_title)}' to your list.",
                "tool_calls": [{"name": "add_task", "arguments": {"user_id": user_id, "title": task_title}}]
            }

    elif ("show" in last_message or "list" in last_message or "display" in last_message or
          "all my tasks" in last_message or
          ("what" in last_message and ("task" in last_message or "pending" in last_message or "complete" in last_message or "all" in last_message)) or
          ("show" in last_message and "task" in last_message) or
          ("all" in last_message and "pending" in last_message) or
          ("what" in last_message and "pending" in last_message) or
          ("my" in last_message and "pending" in last_message and "task" in last_message)):
        # Determine status to filter
        status = "all"
        if "pending" in last_message:
            status = "pending"
        elif "complete" in last_message or "done" in last_message:
            status = "completed"

        # Call list_tasks MCP tool
        result = await send_mcp_request("list_tasks", {
            "user_id": user_id,
            "status": status
        })

        if "error" in result:
            return {
                "response": f"Sorry, I encountered an error: {result['error']}",
                "tool_calls": []
            }
        else:
            if result:
                task_descriptions = []
                for task in result:
                    status_text = 'completed' if task.get('completed', False) else 'pending'
                    # Format as expected by frontend for parsing
                    task_descriptions.append(f"Task #{task['id']}: '{task['title']}' ({status_text})")

                tasks_text = "\n".join(task_descriptions)
                response = f"Here are your {status} tasks:\n{tasks_text}"
            else:
                response = f"You don't have any {status} tasks."

            return {
                "response": response,
                "tool_calls": [{"name": "list_tasks", "arguments": {"user_id": user_id, "status": status}}]
            }

    elif ("complete" in last_message or "done" in last_message or "finish" in last_message) and ("task" in last_message):
        # Extract task ID from the message - handle variations like "task no 8", "task #8", "task 8"
        import re
        # Look for patterns like "task 8", "task no 8", "task No 9", "task #8", etc.
        match = re.search(r'task\s+(?:[Nn]o\s+|#)?(\d+)', last_message)
        if match:
            task_id = int(match.group(1))

            # Call complete_task MCP tool
            result = await send_mcp_request("complete_task", {
                "user_id": user_id,
                "task_id": task_id
            })

            if "error" in result:
                return {
                    "response": f"Sorry, I encountered an error: {result['error']}",
                    "tool_calls": []
                }
            else:
                return {
                    "response": f"I've marked the task '{result.get('title', 'unnamed')}' as completed.",
                    "tool_calls": [{"name": "complete_task", "arguments": {"user_id": user_id, "task_id": task_id}}]
                }
        else:
            return {
                "response": "I couldn't identify which task to complete. Please specify the task number.",
                "tool_calls": []
            }

    elif "delete" in last_message or "remove" in last_message:
        # Extract task ID from the message
        import re
        match = re.search(r'task\s+(\d+)', last_message)
        if match:
            task_id = int(match.group(1))

            # Call delete_task MCP tool
            result = await send_mcp_request("delete_task", {
                "user_id": user_id,
                "task_id": task_id
            })

            if "error" in result:
                return {
                    "response": f"Sorry, I encountered an error: {result['error']}",
                    "tool_calls": []
                }
            else:
                return {
                    "response": f"I've deleted the task '{result.get('title', 'unnamed')}'.",
                    "tool_calls": [{"name": "delete_task", "arguments": {"user_id": user_id, "task_id": task_id}}]
                }
        else:
            return {
                "response": "I couldn't identify which task to delete. Please specify the task number.",
                "tool_calls": []
            }

    elif "update" in last_message or "change" in last_message or "rename" in last_message:
        # Extract task ID and new title from the message
        import re
        task_match = re.search(r'task\s+(\d+)', last_message)
        title_match = re.search(r'(?:to|as)\s+(.+?)(?:\.|$)', last_message)

        if task_match and title_match:
            task_id = int(task_match.group(1))
            new_title = title_match.group(1).strip()

            # Call update_task MCP tool
            result = await send_mcp_request("update_task", {
                "user_id": user_id,
                "task_id": task_id,
                "title": new_title
            })

            if "error" in result:
                return {
                    "response": f"Sorry, I encountered an error: {result['error']}",
                    "tool_calls": []
                }
            else:
                return {
                    "response": f"I've updated the task to '{result.get('title', new_title)}'.",
                    "tool_calls": [{"name": "update_task", "arguments": {"user_id": user_id, "task_id": task_id, "title": new_title}}]
                }
        else:
            return {
                "response": "I couldn't identify which task to update or what to change it to. Please specify both the task number and the new title.",
                "tool_calls": []
            }

    else:
        # Default response for unrecognized commands
        return {
            "response": "I'm your AI assistant for managing todos. You can ask me to add, list, complete, delete, or update tasks.",
            "tool_calls": []
        }