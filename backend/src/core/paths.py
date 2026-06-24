import os

RAW_DOCUMENT = os.getenv("RAW_DOCUMENT", "./data/raw/raw_ai.txt")
PROCESSED_DOCUMENT = os.getenv("PROCESSED_DOCUMENT", "./data/processed/processed_ai.txt")
EMBEDDING_CACHE = os.getenv("EMBEDDING_CACHE", "./data/embedding_cache")
VECTORSTORE = os.getenv("VECTORSTORE", "./vectorstore/FAISS_db")
EVALUATION = os.getenv("EVALUATION", "./data/evaluation")