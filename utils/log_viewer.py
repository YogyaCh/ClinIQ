import json
import os
from statistics import mean
import argparse

EVAL_LOG_PATH = "logs/eval_log.jsonl"
MONITOR_LOG_PATH = "logs/monitor_log.jsonl"

def read_jsonl(path):
    if not os.path.exists(path):
        print(f"[⚠️] File not found: {path}")
        return []
    with open(path, "r") as f:
        return [json.loads(line) for line in f if line.strip()]

def summarize_evaluation():
    logs = read_jsonl(EVAL_LOG_PATH)
    f1_scores = [entry['result'].get('F1') for entry in logs if 'F1' in entry['result']]
    ocr_scores = [entry['result'] for entry in logs if entry['type'] == 'ocr' and isinstance(entry['result'], (int, float))]

    print("\n📊 Evaluation Summary")
    if f1_scores:
        print(f"Avg BERTScore F1: {mean(f1_scores):.4f} ({len(f1_scores)} entries)")
    if ocr_scores:
        print(f"Avg OCR score: {mean(ocr_scores):.2f} ({len(ocr_scores)} entries)")

def summarize_monitoring():
    logs = read_jsonl(MONITOR_LOG_PATH)
    timings = [entry['metadata']['duration_sec'] for entry in logs if entry['event'] == 'timing']
    errors = [entry for entry in logs if 'error' in entry['event'].lower()]

    print("\nMonitoring Summary")
    if timings:
        print(f"Avg stage duration: {mean(timings):.2f}s ({len(timings)} entries)")
    print(f"❌ Errors recorded: {len(errors)}")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--eval", action="store_true", help="Summarize evaluation logs")
    parser.add_argument("--monitor", action="store_true", help="Summarize monitoring logs")
    args = parser.parse_args()

    if args.eval:
        summarize_evaluation()
    if args.monitor:
        summarize_monitoring()
    if not args.eval and not args.monitor:
        summarize_evaluation()
        summarize_monitoring()

if __name__ == "__main__":
    main()
