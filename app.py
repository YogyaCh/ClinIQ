from flask import Flask, render_template, request, redirect, url_for
from celery.result import AsyncResult
from celery_worker import run_pipeline
from logger import get_logger, log_timing
from utils.utils import is_pdf_empty

import os

logger = get_logger()
app = Flask(__name__)
UPLOAD_FOLDER = 'data/reports/'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/', methods=['GET', 'POST'])
@log_timing
def index():
    if request.method == 'POST':
        file = request.files.get('pdf')
        if file:
            filename = file.filename
            file_path = os.path.join(UPLOAD_FOLDER, filename)
            file.save(file_path)

            logger.info(f"Received file upload: {filename}")
            if is_pdf_empty(file_path):
                logger.warning(f"Empty or unreadable PDF uploaded: {file_path}")
                return render_template("error.html", error_message="The uploaded PDF is empty or unreadable. Please check the file and try again.")


            task = run_pipeline.delay(file_path)
            logger.info(f"Task {task.id} submitted for file {filename}")
            return redirect(url_for('result', task_id=task.id))

    return render_template("index.html", summary=None, ocr_text=None, show_text=False, filename=None)

@app.route('/result/<task_id>')
@log_timing
def result(task_id):
    task: AsyncResult = run_pipeline.AsyncResult(task_id)
    logger.debug(f"Checking status for task: {task_id}")

    if task.state == 'PENDING':
        return render_template("loading.html", message="Task queued. Please wait...")

    elif task.state == 'STARTED':
        return render_template("loading.html", message="Processing your report...")

    elif task.state == 'SUCCESS':
        result = task.result
        logger.info(f"Task {task_id} completed successfully")
        return render_template("index.html", summary=result["summary"], ocr_text=result["text"],
                               show_text=True, filename=None)

    elif task.state == 'FAILURE':
        logger.error(f"Task {task_id} failed with error: {task.info}")
        return render_template("error.html", message=str(task.info))

    logger.warning(f"Unexpected task state: {task.state}")
    return "Unexpected state."




#ToDo
@app.route('/health')
def health():
    logger.info("Health check OK")
    return {"status": "ok"}, 200

@app.route('/metrics')
def metrics():
    return {"status": "ok", "metrics": "coming soon"}
