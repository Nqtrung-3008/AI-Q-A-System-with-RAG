from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel.ext.asyncio.session import AsyncSession
from backend.src.dependencies import get_session, get_current_user
from backend.src.crud import crud_conversations
from backend.src.schemas.schemas import ConversationCreate

router = APIRouter()

@router.post('/')
async def create_session(conversation_data: ConversationCreate,
                         session: AsyncSession=Depends(get_session),
                         user=Depends(get_current_user)):
    
    return await crud_conversations.create_conversation(conversation_data=conversation_data, user_id=user.user_id, session=session)

@router.get('/')
async def get_sessions(session: AsyncSession=Depends(get_session),
                       user=Depends(get_current_user)):
    return await crud_conversations.get_conversations_by_user(user_id=user.user_id, session=session)

@router.delete('/{conversation_id}')
async def delete_sessions(conversation_id: int,
                          session: AsyncSession=Depends(get_session),
                          user=Depends(get_current_user)):
    return await crud_conversations.delete_conversation(conversation_id=conversation_id, user_id=user.user_id, session=session)
