import logging
from typing import Optional
from src.config import config

try:
    from langdetect import detect_langs
    from langdetect.lang_detect_exception import LangDetectException
    LANGDETECT_AVAILABLE = True
except ImportError:
    detect_langs = None
    LangDetectException = Exception
    LANGDETECT_AVAILABLE = False

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def language_filter(record: dict) -> Optional[dict]:
    text = record.get("text", "")
    if not text:
        return None

    if not LANGDETECT_AVAILABLE:
        logger.warning("langdetect not available, skipping language filter")
        return None

    try:
        langs = detect_langs(text)
    except Exception as e:
        logger.warning(f"Language detection failed: {e}")
        return None

    for lang in langs:
        if lang.lang == "en" and lang.prob >= config.lang_filter_threshold:
            return record

    return None
