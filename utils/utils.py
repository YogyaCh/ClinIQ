import fitz  # PyMuPDF

def is_pdf_empty(path):
    try:
        doc = fitz.open(path)
        if len(doc) == 0:
            return True  # No pages

        for page in doc:
            text = page.get_text().strip()
            if text:
                return False  # Found non-empty text

        return True  # All pages blank
    except Exception:
        return True  # If unreadable, treat as empty