from celery import Celery
from celery.utils.log import get_task_logger
from backend.ocr import extract_text
from backend.summary import generate_summary
from backend.retrieval import get_contextual_knowledge
import time

logger = get_task_logger(__name__)

celery_app = Celery(
    "clinIQ-tasks",
    broker="redis://redis:6379/0",
    backend="redis://redis:6379/0"
)

@celery_app.task(bind=True, max_retries=3, autoretry_for=(Exception,), retry_backoff=True, retry_jitter=True)
def run_pipeline(self, file_path: str, category: str = "Hematology"):
    task_id = self.request.id
    try:
        logger.info(f"[{task_id}] Starting pipeline for: {file_path}")

        text = extract_text(file_path, task_id=task_id)
        context = get_contextual_knowledge(category, task_id=task_id)
        summary = generate_summary(text, context, task_id=task_id)

        logger.info(f"[{task_id}] Completed pipeline for: {file_path}")
        return {"text": text, "summary": summary}

    except Exception as e:
        logger.error(f" [{task_id}] Error in pipeline for {file_path}: {e}")
        raise self.retry(exc=e)