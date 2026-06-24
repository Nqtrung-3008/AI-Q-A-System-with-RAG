from typing import List
from sqlmodel import SQLModel
from datetime import datetime

class UserBase(SQLModel):
    username: str
    
class UserRegister(UserBase):
    username: str
    password: str
    
class UserPublic(UserBase):
    id: int

class UserLogin(UserBase):
    username: str
    password: str

class Token(SQLModel):
    access_token: str
    token_type: str = "bearer"
    
class ConversationBase(SQLModel):
    pass
    
class ConversationCreate(ConversationBase):
    pass
    
class ConversationPublic(ConversationBase):
    id: int
    user_id: int
    created_at: datetime
    
class MessageBase(SQLModel):
    content: str
    role: str
    
class MessageCreate(MessageBase):
    conversation_id: int
    
class MessagePublic(MessageBase):
    id: int
    conversation_id: int
    created_at: datetime
    
class ChatRequest(SQLModel):
    query: str
    conversation_id: int