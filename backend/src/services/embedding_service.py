from typing import List
from langchain_community.vectorstores import FAISS
from langchain_classic.embeddings import CacheBackedEmbeddings
from langchain_classic.storage import LocalFileStore
from backend.src.db.vectorstore import get_embedding_model

def vector_db(chunks: List,
              persist_directory: str):
    store = LocalFileStore(persist_directory)
    cached_embedding = CacheBackedEmbeddings.from_bytes_store(
        underlying_embeddings = get_embedding_model(),
        document_embedding_cache = store,
    )
    
    db = FAISS.from_documents(
        documents = chunks,
        embedding = cached_embedding
    )
    
    return db