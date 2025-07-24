
from pathlib import Path
import json

LOG_FILE = Path("outputs/logs.jsonl")

def log_interaction(query, context, generated_answer, ground_truth=None):
    interaction = {
        "query": query,
        "contexts": [context],
        "generated_answer": generated_answer,
        "ground_truth": ground_truth,
    }
    LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(LOG_FILE, "a") as f:
        f.write(json.dumps(interaction) + "\n")

def run_ragas_evaluation():
    import pandas as pd
    from datasets import Dataset
    from ragas import evaluate
    from ragas.metrics import (
        faithfulness,
        answer_relevancy,
        context_precision,
        context_recall
    )

    if not LOG_FILE.exists():
        raise FileNotFoundError("logs.jsonl file not found in outputs/")

    with open(LOG_FILE, "r") as f:
        data = [json.loads(line) for line in f]

    dataset = Dataset.from_list(data)

    results = evaluate(
        dataset,
        metrics=[
            faithfulness,
            answer_relevancy,
            context_precision,
            context_recall
        ]
    )

    return results
