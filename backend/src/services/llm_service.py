from core.config import settings
from typing import List
from langchain_ollama import OllamaLLM  
prompt_template = """
You are a senior AI engineer and technical educator.

You help users understand AI concepts using ONLY the provided context.

STRICT RULES:
- Only use information inside <documents>.
- Never use external knowledge.
- Do not guess or infer missing facts.
- If the context is insufficient, say:
  "I don't have enough information in the provided context."

CITATION RULE:
- Every factual claim MUST include citation in the format [chunk:{chunk_id}]
- If multiple chunks are used, cite all relevant chunk_ids
- Do not make any uncited claims

RESPONSE STYLE:
- Clear and educational
- Prefer simple explanations
- Use bullet points when helpful
- Be concise

---

<documents>
{context}
</documents>

---

Question:
{question}

Answer:
"""

def get_context(docs, history: list | None = None):
    
    doc_context = "\n".join(
        f"""[chunk_id={doc.metadata.get('chunk_id', '')} | source={doc.metadata.get('source', '')}]
            {doc.page_content}"""
        for doc in docs
    )

    history_context = ""

    if history:
        history_context = "\n".join(
            f"{msg.role}: {msg.content}"
            for msg in history
        )

    context = f"""
        DOCUMENTS:
        {doc_context}

        CHAT HISTORY:
        {history_context}
        """

    return context
    
_model = None

def get_model():
    global _model
    if _model is None:
        _model = OllamaLLM(
            model=settings.OLLAMA_LLM_MODEL,
            base_url=settings.OLLAMA_BASE_URL,
        )
    return _model

def get_result(model,
               query: str,
               context: str):
    prompt = prompt_template.format(
        question = query,
        context = context
    )
    result  = model.invoke(prompt)
    
    return result