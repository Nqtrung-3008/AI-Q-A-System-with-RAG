from langchain_core.vectorstores import VectorStore
from langchain_core.documents import Document
from backend.src.core.config import settings

def retrieve_documents(
    db: VectorStore,
    query: str,
    k: int = settings.TOP_K
) -> list[Document]:
    return db.similarity_search_with_score(query,k)