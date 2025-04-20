import requests
import time
from logger import get_logger

logger = get_logger()

#OLLAMA_API_URL = "http://localhost:11434/api/generate"
OLLAMA_API_URL = "http://host.docker.internal:11434/api/generate"

def query_ollama(prompt: str, model: str = "llama3") -> str:
    payload = {
        "model": model,
        "prompt": prompt,
        "stream": False
    }

    logger.info(f"Calling Ollama model: {model}, prompt length: {len(prompt)} chars")

    try:
        start = time.time()
        response = requests.post(OLLAMA_API_URL, json=payload, timeout=120)
        response.raise_for_status()
        result = response.json()["response"].strip()
        logger.info(f"Ollama responded in {time.time() - start:.2f}s")
        return result

    except requests.exceptions.RequestException as e:
        logger.error(f"Ollama API call failed: {e}")
        return " Error: Could not generate response from local model."

# Generate Summary Prompt
def generate_summary_response(report_text: str, knowledge: str, model: str = "llama3") -> str:
    prompt = f"""
        You are a helpful medical assistant AI.

        Summarize the abnormalities found in the following lab report using the provided medical knowledge.

        LAB REPORT:
        {report_text}

        KNOWLEDGE:
        {knowledge}

        Your summary should list any abnormal values, mention relevant biomarkers, and provide insights as needed.
    """
    return query_ollama(prompt, model=model)

# Generate Answer for Q&A
def generate_qa_response(report_text: str, user_question: str, knowledge: str, model: str = "llama3") -> str:
    prompt = f"""
        You are a helpful medical assistant AI.

        Use the lab report and the background knowledge to answer the user's question.

        LAB REPORT:
        {report_text}

        KNOWLEDGE:
        {knowledge}

        USER QUESTION:
        {user_question}

        Answer:
    """
    return query_ollama(prompt, model=model)
