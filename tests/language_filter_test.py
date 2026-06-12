from unittest.mock import patch
from langdetect.lang_detect_exception import LangDetectException
from src.pipeline.language_filter import language_filter


def test_english_passes():
    record = {
        "text": "The quick brown fox jumps over the lazy dog.",
        "url": "https://example.com",
        "timestamp": "2024-01-01",
    }
    result = language_filter(record)
    assert result is not None
    assert result == record


def test_french_fails():
    record = {
        "text": "Bonjour le monde, ceci est un texte en français.",
        "url": "https://example.com",
        "timestamp": "2024-01-01",
    }
    result = language_filter(record)
    assert result is None


def test_empty_text_fails():
    record = {
        "text": "",
        "url": "https://example.com",
        "timestamp": "2024-01-01",
    }
    result = language_filter(record)
    assert result is None


@patch("src.pipeline.language_filter.detect_langs")
def test_langdetect_exception_returns_none(mock_detect_langs):
    mock_detect_langs.side_effect = LangDetectException("error", "test error")
    record = {
        "text": "Some text here.",
        "url": "https://example.com",
        "timestamp": "2024-01-01",
    }
    result = language_filter(record)
    assert result is None
