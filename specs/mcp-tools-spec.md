# Todo AI Chatbot - MCP Tools Specification

## Overview
This document specifies the Model Context Protocol (MCP) tools exposed by the Todo AI Chatbot's MCP server for use by AI agents.

## Server Information
- Server Name: `todo-mcp-server`
- Protocol: MCP (Model Context Protocol)
- Transport: Standard I/O (stdio) or HTTP

## Available Tools

### 1. add_task
**Purpose**: Create a new task

**Input Schema**:
```json
{
  "type": "object",
  "properties": {
    "user_id": {
      "type": "string",
      "description": "User identifier"
    },
    "title": {
      "type": "string",
      "description": "Task title"
    },
    "description": {
      "type": "string",
      "description": "Task description (optional)"
    }
  },
  "required": ["user_id", "title"]
}
```

**Output**:
```json
{
  "type": "object",
  "properties": {
    "task_id": {
      "type": "integer",
      "description": "The ID of the created task"
    },
    "status": {
      "type": "string",
      "enum": ["created"],
      "description": "Status of the operation"
    },
    "title": {
      "type": "string",
      "description": "Title of the created task"
    }
  }
}
```

**Example Input**:
```json
{
  "user_id": "ziakhan",
  "title": "Buy groceries",
  "description": "Milk, eggs, bread"
}
```

**Example Output**:
```json
{
  "task_id": 5,
  "status": "created",
  "title": "Buy groceries"
}
```

### 2. list_tasks
**Purpose**: Retrieve tasks from the list

**Input Schema**:
```json
{
  "type": "object",
  "properties": {
    "user_id": {
      "type": "string",
      "description": "User identifier"
    },
    "status": {
      "type": "string",
      "enum": ["all", "pending", "completed"],
      "description": "Filter tasks by status (optional, defaults to 'all')"
    }
  },
  "required": ["user_id"]
}
```

**Output**:
```json
{
  "type": "array",
  "items": {
    "type": "object",
    "properties": {
      "id": {
        "type": "integer",
        "description": "Task ID"
      },
      "title": {
        "type": "string",
        "description": "Task title"
      },
      "completed": {
        "type": "boolean",
        "description": "Whether the task is completed"
      }
    }
  }
}
```

**Example Input**:
```json
{
  "user_id": "ziakhan",
  "status": "pending"
}
```

**Example Output**:
```json
[
  {
    "id": 1,
    "title": "Buy groceries",
    "completed": false
  },
  {
    "id": 2,
    "title": "Call mom",
    "completed": false
  }
]
```

### 3. complete_task
**Purpose**: Mark a task as complete

**Input Schema**:
```json
{
  "type": "object",
  "properties": {
    "user_id": {
      "type": "string",
      "description": "User identifier"
    },
    "task_id": {
      "type": "integer",
      "description": "Task identifier"
    }
  },
  "required": ["user_id", "task_id"]
}
```

**Output**:
```json
{
  "type": "object",
  "properties": {
    "task_id": {
      "type": "integer",
      "description": "The ID of the completed task"
    },
    "status": {
      "type": "string",
      "enum": ["completed"],
      "description": "Status of the operation"
    },
    "title": {
      "type": "string",
      "description": "Title of the completed task"
    }
  }
}
```

**Example Input**:
```json
{
  "user_id": "ziakhan",
  "task_id": 3
}
```

**Example Output**:
```json
{
  "task_id": 3,
  "status": "completed",
  "title": "Call mom"
}
```

### 4. delete_task
**Purpose**: Remove a task from the list

**Input Schema**:
```json
{
  "type": "object",
  "properties": {
    "user_id": {
      "type": "string",
      "description": "User identifier"
    },
    "task_id": {
      "type": "integer",
      "description": "Task identifier"
    }
  },
  "required": ["user_id", "task_id"]
}
```

**Output**:
```json
{
  "type": "object",
  "properties": {
    "task_id": {
      "type": "integer",
      "description": "The ID of the deleted task"
    },
    "status": {
      "type": "string",
      "enum": ["deleted"],
      "description": "Status of the operation"
    },
    "title": {
      "type": "string",
      "description": "Title of the deleted task"
    }
  }
}
```

**Example Input**:
```json
{
  "user_id": "ziakhan",
  "task_id": 2
}
```

**Example Output**:
```json
{
  "task_id": 2,
  "status": "deleted",
  "title": "Old task"
}
```

### 5. update_task
**Purpose**: Modify task title or description

**Input Schema**:
```json
{
  "type": "object",
  "properties": {
    "user_id": {
      "type": "string",
      "description": "User identifier"
    },
    "task_id": {
      "type": "integer",
      "description": "Task identifier"
    },
    "title": {
      "type": "string",
      "description": "New task title (optional)"
    },
    "description": {
      "type": "string",
      "description": "New task description (optional)"
    }
  },
  "required": ["user_id", "task_id"]
}
```

**Output**:
```json
{
  "type": "object",
  "properties": {
    "task_id": {
      "type": "integer",
      "description": "The ID of the updated task"
    },
    "status": {
      "type": "string",
      "enum": ["updated"],
      "description": "Status of the operation"
    },
    "title": {
      "type": "string",
      "description": "Updated title of the task"
    }
  }
}
```

**Example Input**:
```json
{
  "user_id": "ziakhan",
  "task_id": 1,
  "title": "Buy groceries and fruits"
}
```

**Example Output**:
```json
{
  "task_id": 1,
  "status": "updated",
  "title": "Buy groceries and fruits"
}
```

## Error Handling
All tools should return appropriate error responses when:
- Invalid parameters are provided
- User authentication fails
- Task does not exist
- Database errors occur