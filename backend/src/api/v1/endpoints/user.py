from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel.ext.asyncio.session import AsyncSession
from backend.src.dependencies import get_session, get_current_user
from backend.src.crud import crud_users

router = APIRouter()

@router.get('/me')
async def get_me(current_user=Depends(get_current_user)):
    return current_user

@router.get('/{username}')
async def get_me(username: str, session=Depends(get_session)):
    return await crud_users.get_user_by_username(username=username, session=session)

@router.get('/{user_id}')
async def get_me(user_id:int, session=Depends(get_session)):
    return await crud_users.get_user_by_id(user_id=user_id, session=session)