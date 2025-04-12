from rapidfuzz import fuzz
from bert_score import score as bert_score
from typing import Optional, Tuple
import logging
import json
from datetime import datetime

logger = logging.getLogger(__name__)

def evaluate_ocr(predicted_text: str, reference_text: str) -> float:
    """
    Fuzzy string similarity between OCR output and reference.
    """
    score = fuzz.token_sort_ratio(predicted_text, reference_text)
    logger.info(f"OCR Evaluation: Fuzzy score = {score}")
    return score

def evaluate_summary(predicted: str, reference: str, lang: str = "en") -> Tuple[float, float, float]:
    """
    Semantic similarity between LLM summary and human summary using BERTScore.
    Returns precision, recall, F1
    """
    P, R, F1 = bert_score([predicted], [reference], lang=lang, verbose=False)
    logger.info(f"Summary Evaluation - P: {P[0]:.4f}, R: {R[0]:.4f}, F1: {F1[0]:.4f}")
    return P[0].item(), R[0].item(), F1[0].item()

# Save evaluation logs to JSON

def log_evaluation_result(task_type: str, input_file: str, result: dict):
    """
    Save evaluation result to a JSONL file (append-mode)
    """
    log_path = "logs/eval_log.jsonl"
    entry = {
        "timestamp": datetime.utcnow().isoformat(),
        "type": task_type,
        "input": input_file,
        "result": result
    }
    with open(log_path, "a") as f:
        f.write(json.dumps(entry) + "\n")
