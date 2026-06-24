from datetime import datetime
import os

from backend.src.utils.helpers import preprocessing_document
from backend.src.utils.loaders import load_document
from backend.src.utils.chunking import chunking
from backend.src.core.paths import RAW_DOCUMENT, PROCESSED_DOCUMENT, EMBEDDING_CACHE, VECTORSTORE
from backend.src.services.embedding_service import vector_db
from backend.src.db.vectorstore import save_db

def main(): 
    preprocessing_document(RAW_DOCUMENT, PROCESSED_DOCUMENT)
    
    document = load_document(PROCESSED_DOCUMENT)
    
    chunks = chunking(document)
    
    db = vector_db(chunks, os.path.join(EMBEDDING_CACHE, datetime.now().strftime("%Y%m%d_%H%M%S")))
    
    save_db(db, VECTORSTORE)
    
if __name__ == '__main__':
    main()