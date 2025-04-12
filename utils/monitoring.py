import time
import logging
import json
from datetime import datetime
from typing import Dict, Any

logger = logging.getLogger(__name__)

def monitor_event(event_name: str, metadata: Dict[str, Any]):
    """
    Log a monitoring event with custom metadata.
    Writes to logs/monitor_log.jsonl
    """
    event = {
        "timestamp": datetime.utcnow().isoformat(),
        "event": event_name,
        "metadata": metadata
    }
    log_path = "logs/monitor_log.jsonl"
    with open(log_path, "a") as f:
        f.write(json.dumps(event) + "\n")
    logger.info(f"[MONITOR] {event_name} - {metadata}")

def monitor_timing(stage_name: str):
    """
    Decorator to time and log a processing stage
    """
    def decorator(func):
        def wrapper(*args, **kwargs):
            start = time.time()
            result = func(*args, **kwargs)
            end = time.time()
            duration = end - start
            monitor_event("timing", {"stage": stage_name, "duration_sec": duration})
            return result
        return wrapper
    return decorator
