from backend.src.db.vectorstore import load_db
from backend.src.services.rag_service import run_rag_pipeline
from backend.src.core.paths import VECTORSTORE

db = load_db(VECTORSTORE)

query = 'What are applications of AI in game?'

print(run_rag_pipeline(db, query))