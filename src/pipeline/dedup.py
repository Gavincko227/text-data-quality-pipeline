import logging
from typing import Optional, Set

from datasketch import MinHash, MinHashLSH

from src.config import config

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

_NUM_PERM = 128


def _shingles(text: str, n: int) -> Set[str]:
    words = text.lower().split()
    if not words:
        return set()
    if len(words) < n:
        return {" ".join(words)}
    return {" ".join(words[i : i + n]) for i in range(len(words) - n + 1)}


def _minhash_from_text(text: str) -> MinHash:
    m = MinHash(num_perm=_NUM_PERM)
    for shingle in _shingles(text, config.dedup_shingles):
        m.update(shingle.encode("utf-8"))
    return m


def create_index() -> dict:
    """Create an empty MinHash LSH index for near-duplicate detection."""
    return {
        "lsh": MinHashLSH(threshold=config.dedup_threshold, num_perm=_NUM_PERM),
        "minhashes": {},
        "counter": 0,
    }


def is_duplicate(index: dict, record: dict) -> Optional[dict]:
    """
    Check a record against the dedup index.

    Returns None if the record is >= dedup_threshold similar to an existing entry.
    Otherwise adds the record's MinHash signature to the index and returns the record.
    """
    text = record.get("text", "")
    if not text:
        return None

    minhash = _minhash_from_text(text)
    lsh = index["lsh"]

    for key in lsh.query(minhash):
        existing = index["minhashes"][key]
        if minhash.jaccard(existing) >= config.dedup_threshold:
            return None

    key = str(index["counter"])
    index["counter"] += 1
    index["minhashes"][key] = minhash
    lsh.insert(key, minhash)
    return record
