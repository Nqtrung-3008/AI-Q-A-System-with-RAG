from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel.ext.asyncio.session import AsyncSession
from backend.src.dependencies import get_session, get_current_user
from backend.src.crud import crud_conversations, crud_messages
from backend.src.schemas.schemas import ChatRequest
from backend.src.services.rag_service import run_rag_pipeline
from backend.src.crud.crud_messages import get_messages_by_conversation

router = APIRouter()

@router.post("/chat")
async def chat(
    req: ChatRequest,
    session: AsyncSession = Depends(get_session),
    user=Depends(get_current_user)
):
    conversation = await crud_conversations.get_conversation_by_id(req.conversation_id, session)

    if not conversation:
        raise HTTPException(404, "Session not found")
    if conversation.user_id != user.user_id:
        raise HTTPException(403, "Forbidden")
    
    result = await run_rag_pipeline(
        session=session,
        query=req.query,
        user_id=user.user_id,
        conversation_id=req.conversation_id
    )

    return {"answer": result}

@router.get("/messages/{conversation_id}")
async def get_messages(conversation_id: int, 
                       session: AsyncSession = Depends(get_session),
                       user=Depends(get_current_user)
                       ):
    return await crud_messages.get_messages_by_conversation(conversation_id=conversation_id, user_id=user.user_id, session=session)