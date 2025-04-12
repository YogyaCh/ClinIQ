from api.local_llm import generate_summary_response, generate_qa_response
from logger import get_logger, log_timing

logger = get_logger()

@log_timing
def generate_summary(report_text: str, knowledge: str) -> str:
    logger.info(f"Generating summary using local LLM (report length: {len(report_text)} chars)")
    try:
        return generate_summary_response(report_text, knowledge, model="llama3")
    except Exception as e:
        logger.error(f"Error generating summary: {e}")
        raise e

@log_timing
def answer_question(report_text: str, question: str, knowledge: str) -> str:
    logger.info(f"Answering question: '{question}' (report length: {len(report_text)} chars)")
    try:
        return generate_qa_response(report_text, question, knowledge, model="llama3")
    except Exception as e:
        logger.error(f"Error answering question: {e}")
        raise e
