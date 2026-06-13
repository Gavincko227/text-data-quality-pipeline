import logging
import string
from typing import Optional
from src.config import config

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def quality_score(record: dict) -> Optional[dict]:
    text = record.get("text", "")
    if not text:
        record["quality_scores"] = {}
        record["quality_passed"] = False
        return record

    words = text.split()
    doc_length = len(words) #number of words

    avg_word_length = (
        sum(len(w) for w in words) / len(words) if words else 0
    )

    punct_count = sum(1 for ch in text if ch in string.punctuation)
    punct_ratio = punct_count / doc_length if doc_length > 0 else 0

    digit_count = sum(1 for ch in text if ch.isdigit())
    digit_ratio = digit_count / doc_length if doc_length > 0 else 0

    quality_scores = {
        "doc_length": doc_length,
        "average_word_length": round(avg_word_length, 4),
        "punctuation_ratio": round(punct_ratio, 4),
        "digit_ratio": round(digit_ratio, 4),
    }

    quality_passed = (
        config.min_doc_length <= doc_length <= config.max_doc_length
        and config.min_avg_word_length <= avg_word_length <= config.max_avg_word_length
        and punct_ratio <= config.max_punctuation_ratio
        and digit_ratio <= config.max_digit_ratio
    )

    record["quality_scores"] = quality_scores
    record["quality_passed"] = quality_passed
    return record
