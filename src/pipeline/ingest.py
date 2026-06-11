

import logging
import datasets
from typing import Generator

from src.config import config


# Initialize logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


# Generator function to yield records
def generate_records() -> Generator[dict, None, None]:
    """
    Streams records from allenai/c4 English dataset.
    Yields one record at a time up to 50,000 records.
    """
    dataset = datasets.load_dataset("allenai/c4", "en", streaming=True)
    for i, record in enumerate(dataset["train"]):
        if i == 50000:
            break
        if i > 0 and i % 1000 == 0:
            logger.info(f"Processed {i} records")
        yield record
