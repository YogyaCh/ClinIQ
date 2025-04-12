import pytest
import os
from backend.ocr import extract_text

TEST_PDF_PATH = "tests/sample.pdf"  # Add a real small test PDF here

@pytest.mark.ocr
def test_extract_text_returns_str():
    if not os.path.exists(TEST_PDF_PATH):
        pytest.skip("Test PDF not found.")

    text = extract_text(TEST_PDF_PATH)
    assert isinstance(text, str)
    assert len(text.strip()) > 0, "OCR returned empty string"