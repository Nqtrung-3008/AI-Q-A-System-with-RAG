from fastapi import APIRouter
from backend.src.api.v1.endpoints import auth, conversation, message, user

router = APIRouter()
router.include_router(auth.router, prefix="/auth", tags=["auth"])
router.include_router(message.router, prefix="/messages", tags=["messages"])
router.include_router(conversation.router, prefix="/conversations", tags=["conversation"])
router.include_router(user.router, prefix="/users", tags=["users"])