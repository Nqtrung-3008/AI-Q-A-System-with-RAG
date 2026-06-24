from backend.src.services.retriever_service import retrieve_documents
from backend.src.services.llm_service import get_context, get_model, get_result
from backend.src.crud import crud_messages
from backend.src.schemas.schemas import MessageCreate
from sqlmodel.ext.asyncio.session import AsyncSession
from backend.src.core.paths import VECTORSTORE
from backend.src.db.vectorstore import load_db
from backend.src.core.config import settings

db = load_db(VECTORSTORE)

async def run_rag_pipeline(
    session: AsyncSession,
    query: str,
    user_id: int,
    conversation_id: int,
    k: int = settings.TOP_K
):
    msg = MessageCreate(conversation_id=conversation_id, role='user', content=query)
    
    await crud_messages.create_message(
        message_data=msg,
        session=session
    )
    
    docs = retrieve_documents(db, query, k)
    
    history = await crud_messages.get_last_messages(conversation_id=conversation_id, session=session)
    
    context = get_context(docs, history)
    model = get_model()
    
    result = get_result(model, query, context)
    
    msg = MessageCreate(conversation_id=conversation_id, role='assistant', content=result)
    
    await crud_messages.create_message(
        message_data=msg,
        session=session
    )
    
    return result