import os
import pytest


def test_empty_pdf_upload_shows_error(client):
    empty_pdf_path = os.path.join("data/reports/", "EmptyDoc.pdf")
    with open(empty_pdf_path, "rb") as f:
        response = client.post("/", data={"pdf": f}, follow_redirects=True)
    assert b"empty or unreadable" in response.data
