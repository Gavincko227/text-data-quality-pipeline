from typing import Dict
import os


class Config:
    def __init__(self):
        self.lang_filter_threshold = 0.95
        self.min_doc_length = 10
        self.max_doc_length = 1000
        self.min_avg_word_length = 3
        self.max_avg_word_length = 10
        self.max_punctuation_ratio = 0.1
        self.max_digit_ratio = 0.1
        self.punctuation_ratio = 0.1
        self.digit_ratio = 0.1
        self.dedup_threshold = 0.8
        self.dedup_shingles = 5
        self.pii_entities = ["EMAIL_ADDRESS", "PHONE_NUMBER", "PERSON"]
        self.s3_bucket = "my-bucket"
        self.s3_endpoint_url = "http://localhost:9000"
        self.s3_access_key = "access_key"
        self.s3_secret_key = "secret_key"
        self.output_parquet_path = "output/data.parquet"
        self.output_manifest_path = "output/manifest.json"

config = Config()
