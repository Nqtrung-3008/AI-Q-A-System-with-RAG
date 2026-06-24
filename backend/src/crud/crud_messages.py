from typing import List
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
from backend.src.models.models import Message
from backend.src.schemas.schemas import MessageCreate

async def create_message(message_data: MessageCreate, session: AsyncSession) -> Message:
    db_mesasge = Message.model_validate(message_data)
    session.add(db_mesasge)
    await session.commit()
    await session.refresh(db_mesasge)
    return db_mesasge

async def get_messages_by_conversation(conversation_id: int, user_id: int, session: AsyncSession) -> List[Message]:
    statement = select(Message).where(Message.conversation_id == conversation_id).order_by(Message.created_at)
    result = await session.exec(statement)
    return result.all()

async def get_last_messages(conversation_id: int, session: AsyncSession, limit: int = 10) -> List[Message]:
    statement = select(Message).where(Message.conversation_id == conversation_id).order_by(Message.created_at).limit(limit)
    result = await session.exec(statement)
    result = result.all()
    return list(reversed(result))