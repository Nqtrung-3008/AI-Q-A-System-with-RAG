# AI Q&A System with RAG

A retrieval-augmented question answering system for AI-related documents. The project combines a FastAPI backend, PostgreSQL chat persistence, a FAISS vector store, Hugging Face embeddings, Ollama for local LLM generation, and a Streamlit chat UI.

## Features

- User registration and login with JWT authentication.
- Conversation and message history stored in PostgreSQL.
- RAG pipeline using LangChain, FAISS, and `BAAI/bge-base-en-v1.5` embeddings.
- Local LLM responses through Ollama, configured for `mistral:7b` by default.
- Streamlit frontend for login, conversation management, and chat.
- Scripts for document ingestion, evaluation question generation, and retrieval evaluation.

## Project Structure

```text
.
+-- backend/
|   +-- src/
|   |   +-- api/                 # FastAPI routers and endpoints
|   |   +-- core/                # Settings, DB session, security, paths
|   |   +-- crud/                # Database operations
|   |   +-- db/                  # FAISS and embedding model helpers
|   |   +-- models/              # SQLModel database models
|   |   +-- schemas/             # Request/response schemas
|   |   +-- services/            # RAG, retrieval, LLM, embedding services
|   |   +-- utils/               # Loading, cleaning, chunking helpers
|   +-- alembic/                 # Database migrations
|   +-- Dockerfile
|   +-- requirements.txt
+-- frontend/
|   +-- ui.py                    # Streamlit app
|   +-- Dockerfile
|   +-- requirements.txt
+-- scripts/
|   +-- ingest_data.py           # Build processed document and FAISS index
|   +-- eval_rag.py              # Evaluate retrieval recall/MRR
|   +-- test_query.py            # Legacy quick-test script
+-- data/
|   +-- raw/raw_ai.txt           # Source document
|   +-- processed/processed_ai.txt
|   +-- evaluation/              # Test questions and reports
+-- vectorstore/FAISS_db/        # Saved FAISS index
+-- docker-compose.yml
+-- README.md
```

## Runtime Architecture

1. Raw text is loaded from `data/raw/raw_ai.txt`.
2. `scripts/ingest_data.py` cleans the document, chunks it, embeds chunks, caches embeddings, and saves a FAISS index to `vectorstore/FAISS_db`.
3. The FastAPI backend loads the FAISS index at startup.
4. Authenticated users create conversations from the Streamlit UI.
5. Chat requests are sent to `POST /api/v1/messages/chat`.
6. The backend stores the user message, retrieves relevant chunks, combines retrieved context with recent chat history, asks Ollama for an answer, stores the assistant message, and returns the answer.

## Requirements

- Docker and Docker Compose
- Enough disk space for Ollama models and embedding models
- Internet access for first-time dependency/model downloads

For local, non-Docker development you also need Python 3.11.

## Environment Variables

The project uses `.env` at the repository root. Required variables:

```env
DATABASE_URL=postgresql+psycopg://postgres:postgres@postgres:5432/rag_db
SECRET_KEY=replace-with-a-long-random-secret

OLLAMA_BASE_URL=http://ollama:11434
OLLAMA_LLM_MODEL=mistral:7b

CHUNK_SIZE=800
CHUNK_OVERLAP=150

EMBED_MODEL=BAAI/bge-base-en-v1.5
TOP_K=5
```

Docker Compose also sets these path variables for the backend container:

```env
RAW_DOCUMENT=/workspace/data/raw/raw_ai.txt
PROCESSED_DOCUMENT=/workspace/data/processed/processed_ai.txt
EMBEDDING_CACHE=/workspace/data/embedding_cache
VECTORSTORE=/workspace/vectorstore/FAISS_db
EVALUATION=/workspace/data/evaluation
```

## Quick Start With Docker

Build and start all services:

```bash
docker compose build
docker compose up -d
```

Pull the configured Ollama model:

```bash
docker exec -it ollama ollama pull mistral:7b
```

If the FAISS index is missing or stale, run ingestion:

```bash
docker compose exec backend python /workspace/scripts/ingest_data.py
```

Open the apps:

- Frontend: <http://localhost:8501>
- Backend API docs: <http://localhost:8000/docs>
- Ollama: <http://localhost:11434>
- PostgreSQL: `localhost:5432`

Stop the stack:

```bash
docker compose down
```

Remove containers and database/model volumes:

```bash
docker compose down -v --remove-orphans
```

## Backend API

All main API routes are mounted under `/api/v1`.

### Auth

- `POST /api/v1/auth/register`
  - Body: `{ "username": "...", "password": "..." }`
  - Creates a user.

- `POST /api/v1/auth/login`
  - Body: `{ "username": "...", "password": "..." }`
  - Returns a bearer token.

### Conversations

These endpoints require `Authorization: Bearer <token>`.

- `POST /api/v1/conversations/`
  - Creates a conversation for the current user.

- `GET /api/v1/conversations/`
  - Lists current user's conversations.

- `DELETE /api/v1/conversations/{conversation_id}`
  - Soft-deletes a conversation.

### Messages and Chat

These endpoints require `Authorization: Bearer <token>`.

- `POST /api/v1/messages/chat`
  - Body: `{ "query": "...", "conversation_id": 1 }`
  - Runs the RAG pipeline and returns `{ "answer": "..." }`.

- `GET /api/v1/messages/messages/{conversation_id}`
  - Lists messages for a conversation.

## Data Ingestion

Place or update source content in:

```text
data/raw/raw_ai.txt
```

Run:

```bash
docker compose exec backend python /workspace/scripts/ingest_data.py
```

This will:

- Clean and save the processed document to `data/processed/processed_ai.txt`.
- Split the document into chunks with metadata such as `chunk_id`.
- Build embeddings with the configured Hugging Face model.
- Cache embeddings under `data/embedding_cache`.
- Save the FAISS index under `vectorstore/FAISS_db`.

Restart the backend after rebuilding the vector store, because the FAISS index is loaded when `rag_service.py` is imported.

```bash
docker compose restart backend
```

## Evaluation

Run retrieval evaluation:

```bash
docker compose exec backend python /workspace/scripts/eval_rag.py
```

The evaluator reads:

```text
data/evaluation/test_questions_fixed.json
```

and writes:

```text
data/evaluation/evaluation_report.json
```

Current metrics include:

- `recall@5`
- `mrr`

## Local Development

Backend setup:

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r backend\requirements.txt
uvicorn backend.src.main:app --host 0.0.0.0 --port 8000 --reload
```

Frontend setup:

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r frontend\requirements.txt
streamlit run frontend\ui.py
```

For local development outside Docker, adjust `.env` values:

```env
DATABASE_URL=postgresql+psycopg://postgres:postgres@localhost:5432/rag_db
OLLAMA_BASE_URL=http://localhost:11434
```

The Streamlit app currently uses `http://backend:8000` as the backend URL, which is correct inside Docker. For host-local frontend runs, change `API_BASE` in `frontend/ui.py` to `http://localhost:8000`.

## Database Migrations

The backend container runs migrations automatically on startup:

```bash
alembic upgrade head
```

Create a new migration after model changes:

```bash
docker compose exec backend alembic revision --autogenerate -m "describe change"
```

Apply migrations manually:

```bash
docker compose exec backend alembic upgrade head
```

## Notes and Troubleshooting

- If chat fails at startup with a missing vector database error, run `scripts/ingest_data.py` and restart the backend.
- If answers are unavailable, confirm the Ollama container is running and the configured model has been pulled.
- The RAG prompt requires answers to use only retrieved document context and cite chunk IDs.
- `scripts/test_query.py` is a legacy quick-test helper and does not match the current async `run_rag_pipeline` signature.
- The repository contains generated files such as `venv/`, `__pycache__/`, `data/embedding_cache/`, and FAISS indexes. These are runtime artifacts, not source code.
