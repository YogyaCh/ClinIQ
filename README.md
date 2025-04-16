
# ClinIQ – GenAI-Powered Medical Lab Report Analyzer

ClinIQ is a full-stack, production-ready GenAI application that:
- Extracts text from scanned PDF lab reports (CBC, Hematology, Urine, etc.)
- Retrieves contextual medical knowledge from a custom ChromaDB vector store
- Generates intelligent summaries using local LLaMA-based models via [Ollama](https://ollama.com/)
- Supports concurrent users with Celery + Redis task queue
-  Includes test cases, monitoring logs, and evaluation utilities

---

## Project Structure

```
ClinIQ/
├── app.py                 # Main Flask app
├── celery_worker.py       # Celery task runner
├── backend/               # Core logic: OCR, summary, retrieval
├── api/                   # Ollama interface
├── templates/             # HTML templates (index, loading, error)
├── static/                # CSS styles, loader
├── logs/                  # Output and error logs
├── config/                # App config, settings
├── data/                  # Sample reports and medical knowledge
├── Dockerfile             # Production-ready container
├── docker-compose.yaml    # Services: Flask, Celery, Redis
├── requirements.txt       # Python packages
└── README.md              # This file
```
---
## To Do:

* P0 - Evaluation and Monitoring
* P1 - Tests
* P2 - Add confidence levels or flags (green/yellow/red) to indicate summary quality based on extracted text and context.

---

## Quick Start (Local, No Docker)

### 1. Clone the Repo & Create Environment

```bash
git clone https://github.com/your-username/cliniq.git
cd cliniq

conda create -f environment.yaml
```
or

```bash
conda create -n cliniq python=3.10 -y
conda activate cliniq
pip install -r requirements.txt 
```

### 2. Install System Packages

> Required for OCR:
```bash
brew install tesseract    # macOS
sudo apt install tesseract-ocr  # Ubuntu
```

### 3. Run Redis Locally (optional)

```bash
redis-server
```

(Or use Docker: `docker run -p 6379:6379 redis`)

### 4. Run Ollama with LLaMA

```bash
ollama run llama3
```

> Download and preload the model (prompt: "Say hello")

### 5. Start the App

In one terminal:
```bash
python app.py
```

In another terminal:
```bash
celery -A celery_worker worker --loglevel=info
```

Now open [http://localhost:5050](http://localhost:5050)

---

## Quick Start with Docker

### 1. Build and Launch

```bash
docker compose up --build
```

This starts:
- Flask app with Gunicorn (`cliniq_app`)
- Celery worker (`cliniq_celery`)
- Redis queue (`cliniq_redis`)

> Make sure [Ollama](https://ollama.com) is running on your host:  
```bash
ollama run llama3
```

> Update `api/local_llm.py` to:
```python
OLLAMA_API_URL = "http://host.docker.internal:11434/api/generate"
```

---

## Testing

Run all tests using:

```bash
pytest
```

You’ll find:
- `tests/test_summary.py`
- `tests/test_ocr.py`
- `tests/test_pipeline.py`

---

## Features

| Feature                  | Description |
|--------------------------|-------------|
| OCR                   | Extracts text from PDFs using Tesseract |
| LLM Summarization     | Uses local LLaMA (via Ollama) |
| Retrieval             | Contextual vector DB from medical knowledge |
| Async Tasks           | Celery + Redis for concurrency |
| Monitoring            | Logs performance and failures |
| Dockerized            | Runs all services together in production |

---

## Requirements

- Python 3.10+
- Redis
- Tesseract OCR
- Ollama (LLaMA model)
- Docker (optional)

---
