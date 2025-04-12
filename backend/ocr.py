# backend/ocr.py

from pdf2image import convert_from_path
from pytesseract import image_to_string
from PIL import Image
from logger import get_logger, log_timing

logger = get_logger()

@log_timing
def extract_text(pdf_path: str) -> str:
    """
    Extract text from PDF using pytesseract (Tesseract OCR).
    """
    logger.info(f"📄 Starting Tesseract OCR on: {pdf_path}")

    try:
        images = convert_from_path(pdf_path, dpi=300)
        all_text = []
        for i, img in enumerate(images):
            text = image_to_string(img)
            all_text.append(text)
        result = "\n".join(all_text)
        logger.info("✅ Tesseract OCR complete.")
        return result

    except Exception as e:
        logger.error(f"❌ Tesseract OCR failed: {e}")
        raise e

def extract_text_from_image(image_path: str) -> str:
    """
    Uses PaddleOCR to extract text from an image file.
    """
    ocr_results = ocr_engine.ocr(image_path, cls=True)
    full_text = ""
    for line in ocr_results[0]:
        text = line[1][0]
        full_text += text + "\n"

    return full_text.strip()

