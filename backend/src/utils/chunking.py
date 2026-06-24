from typing import Dict
from langchain_text_splitters import RecursiveCharacterTextSplitter
from backend.src.core.config import settings

def chunking(document: Dict,
             chunk_size: int = settings.CHUNK_SIZE,
             chunk_overlap: int = settings.CHUNK_OVERLAP):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size = chunk_size,
        chunk_overlap = chunk_overlap
    )
    
    chunks = text_splitter.split_documents(document)
            
    for i, chunk in enumerate(chunks):
        chunk.metadata.update({
            'chunk_id': i+1,
            'chunk_index': i,
            'chunk_length': len(chunk.page_content),
            'source': chunk.metadata.get('source', '')
        })

    return chunks