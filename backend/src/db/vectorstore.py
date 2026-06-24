import os
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from backend.src.core.config import settings

def get_embedding_model():
    return HuggingFaceEmbeddings(
        model_name=settings.EMBED_MODEL,
        encode_kwargs={"normalize_embeddings": True},
    )

def save_db(db,
            persist_directory: str):    
    db.save_local(persist_directory)

def load_db(persist_directory: str):
    if not os.path.exists(persist_directory):
       raise FileNotFoundError(f'The database does not exist!')
    db = FAISS.load_local(
        persist_directory,
        embeddings = get_embedding_model(),
        allow_dangerous_deserialization=True
    )
    
    return db