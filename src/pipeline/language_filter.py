import logging
from langdetect import detect_langs
from src.config import config

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def language_filter(record: dict) -> dict | None:
    text = record.get("text", "")
    if not text:
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
