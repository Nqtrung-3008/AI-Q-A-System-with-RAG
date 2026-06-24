import json
import os
from typing import List, Dict
from backend.src.db.vectorstore import load_db
from backend.src.core.paths import VECTORSTORE
from backend.src.core.paths import EVALUATION

DATASET_PATH = f"{EVALUATION}/test_questions_fixed.json"
TOP_K = 5
OUTPUT_REPORT = f"{EVALUATION}/evaluation_report.json"

db = load_db(VECTORSTORE)

def retrieve(query: str, top_k = TOP_K, db=db) -> List[int]:
    docs = db.similarity_search(query=query, k=top_k)
    return [doc.metadata["chunk_id"] for doc in docs]

# METRICS
def recall_at_k(retrieved: List[int], relevant: List[int]) -> float:
    if not relevant:
        return 0.0
    return len(set(retrieved) & set(relevant)) / len(relevant)

def mrr(retrieved: List[int], relevant: List[int]) -> float:
    for rank, doc_id in enumerate(retrieved, start=1):
        if doc_id in relevant:
            return 1.0 / rank
    return 0.0

# EVALUATION PIPELINE
def run_evaluation():

    with open(DATASET_PATH, "r", encoding="utf-8") as f:
        dataset = json.load(f)

    total_recall = 0.0
    total_mrr = 0.0
    total_samples = 0

    for sample in dataset:

        question = sample["question"]
        relevant_chunks = sample["relevant_chunk_ids"]

        # 1. Retrieval Evaluation
        retrieved_chunks = retrieve(query=question)

        total_recall += recall_at_k(retrieved_chunks, relevant_chunks)
        total_mrr += mrr(retrieved_chunks, relevant_chunks)

        total_samples += 1

    # FINAL RESULTS
    results = {
        "num_samples": total_samples,
        f"recall@{TOP_K}": total_recall / total_samples,
        "mrr": total_mrr / total_samples,
    }

    # Save report
    with open(OUTPUT_REPORT, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=4)

    print("===== EVALUATION RESULTS =====")
    for k, v in results.items():
        print(f"{k}: {v:.4f}" if isinstance(v, float) else f"{k}: {v}")

    print(f"\nReport saved to {OUTPUT_REPORT}")

if __name__ == "__main__":
    run_evaluation()
