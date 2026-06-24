from sqlalchemy import Column, DateTime
from typing import List, Optional
from sqlmodel import Field, Relationship, SQLModel
from datetime import datetime, timezone

class Users(SQLModel, table = True):
    __tablename__ = "users"
    
    user_id: Optional[int] = Field(default=None, primary_key=True)
    username: str = Field(index=True, unique=True)
    password: str

    conversations: List['Conversation'] = Relationship(back_populates='user')
    
class Conversation(SQLModel, table = True):
    __tablename__ = "conversations"
    
    conversation_id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key='users.user_id')
    created_at: datetime = Field(
        sa_column=Column(DateTime(timezone=True), nullable=False),
        default_factory=lambda: datetime.now(timezone.utc),
    )
    deleted_at: Optional[datetime] = Field(
        default=None,
        sa_column=Column(DateTime(timezone=True), nullable=True),
    )
    user: Users = Relationship(back_populates='conversations')
    messages: List['Message'] = Relationship(back_populates='conversations')
    
class Message(SQLModel, table = True):
    __tablename__ = "messages"
    
    message_id: Optional[int] = Field(default=None, primary_key=True)
    conversation_id: int = Field(foreign_key='conversations.conversation_id')
    created_at: datetime = Field(
        sa_column=Column(DateTime(timezone=True), nullable=False),
        default_factory=lambda: datetime.now(timezone.utc),
    )
    role: str
    content: str
    conversations: Optional[Conversation] = Relationship(back_populates='messages')