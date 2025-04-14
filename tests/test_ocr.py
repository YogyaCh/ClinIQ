import pytest
import os
from backend.ocr import extract_text
from unittest.mock import patch, MagicMock

TEST_PDF_PATH = "data/reports/S1_Haematology_Report.pdf"

@pytest.mark.ocr
def test_extract_text_returns_str():
    if not os.path.exists(TEST_PDF_PATH):
        pytest.skip("Test PDF not found.")

    text = extract_text(TEST_PDF_PATH)
    assert isinstance(text, str)
    assert len(text.strip()) > 0, "OCR returned empty string"

@patch("backend.ocr.convert_from_path")
@patch("backend.ocr.image_to_string")
def test_extract_text_success(mock_image_to_string, mock_convert_from_path):
    # Arrange
    mock_image = MagicMock()
    mock_convert_from_path.return_value = [mock_image, mock_image]
    mock_image_to_string.side_effect = ["Page 1 text", "Page 2 text"]

    # Act
    result = extract_text("fake_path.pdf", task_id="123")

    # Assert
    expected = "Page 1 text\nPage 2 text"
    assert result == expected
    mock_convert_from_path.assert_called_once_with("fake_path.pdf", dpi=300)
    assert mock_image_to_string.call_count == 2

@patch("backend.ocr.convert_from_path", side_effect=Exception("Conversion failed"))
def test_extract_text_failure(mock_convert):
    # Act + Assert
    with pytest.raises(Exception) as exc_info:
        extract_text("invalid.pdf", task_id="fail-test")
    assert "Conversion failed" in str(exc_info.value)