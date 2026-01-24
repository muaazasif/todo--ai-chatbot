from fastapi import APIRouter, HTTPException, BackgroundTasks, Depends
from pydantic import BaseModel
from sqlmodel import Session, select
from models import Message, Conversation, Task, engine, User
from datetime import datetime
from typing import Optional, List
import uuid
from agents import run_agent
from .auth_routes import get_current_user

router = APIRouter()


class ChatRequest(BaseModel):
    conversation_id: Optional[int] = None
    message: str


class ChatResponse(BaseModel):
    conversation_id: int
    response: str
    tool_calls: List[dict] = []


@router.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest, current_user: User = Depends(get_current_user)):
    user_id = current_user.id  # Use the authenticated user's ID

    conversation_id = None

    # Create or get conversation
    with Session(engine) as session:
        if request.conversation_id is None:
            # Create new conversation
            conversation = Conversation(user_id=str(user_id))  # Convert to string to match DB schema
            session.add(conversation)
            session.commit()
            session.refresh(conversation)
            conversation_id = conversation.id
        else:
            conversation_id = request.conversation_id

            # Verify conversation belongs to user
            conversation = session.get(Conversation, request.conversation_id)
            if not conversation or conversation.user_id != user_id:
                raise HTTPException(status_code=404, detail="Conversation not found")

        # Store user message
        user_message = Message(
            user_id=str(user_id),  # Convert to string to match DB schema
            conversation_id=conversation_id,
            role="user",
            content=request.message
        )
        session.add(user_message)
        session.commit()

        # Get conversation history
        statement = select(Message).where(Message.conversation_id == conversation_id).order_by(Message.created_at)
        messages = session.exec(statement).all()

        # Prepare messages for agent
        agent_messages = []
        for msg in messages:
            agent_messages.append({
                "role": msg.role,
                "content": msg.content
            })

    # Run agent with MCP tools
    result = await run_agent(str(user_id), agent_messages)  # Pass user_id as string to match DB schema

    # Store assistant response
    with Session(engine) as session:
        assistant_message = Message(
            user_id=str(user_id),  # Convert to string to match DB schema
            conversation_id=conversation_id,
            role="assistant",
            content=result["response"]
        )
        session.add(assistant_message)
        session.commit()

    return ChatResponse(
        conversation_id=conversation_id,
        response=result["response"],
        tool_calls=result.get("tool_calls", [])
    )