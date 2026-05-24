# config.py
# Centralized config — change one place, affects entire app
# This is how real backends manage environments

import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # Server
    HOST = os.getenv("HOST", "0.0.0.0")
    PORT = int(os.getenv("PORT", 8000))
    DEBUG = os.getenv("DEBUG", "true").lower() == "true"
    ENV = os.getenv("ENV", "development")

    # AI Models
    SENTIMENT_MODEL = os.getenv("SENTIMENT_MODEL", "distilbert-base-uncased-finetuned-sst-2-english")
    SUMMARIZATION_MODEL = os.getenv("SUMMARIZATION_MODEL", "facebook/bart-large-cnn")
    CLASSIFICATION_MODEL = os.getenv("CLASSIFICATION_MODEL", "facebook/bart-large-mnli")

    # Limits
    MAX_TEXT_LENGTH = int(os.getenv("MAX_TEXT_LENGTH", 1000))
    MAX_SUMMARY_LENGTH = int(os.getenv("MAX_SUMMARY_LENGTH", 150))
    MIN_SUMMARY_LENGTH = int(os.getenv("MIN_SUMMARY_LENGTH", 30))

config = Config()