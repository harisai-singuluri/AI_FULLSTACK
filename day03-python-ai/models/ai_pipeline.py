# # models/ai_pipeline.py
# # Central AI/ML pipeline — all model loading and inference happens here
# # IMPORTANT: Models are loaded ONCE at startup, not on every request
# # Loading a model takes 2-5 seconds — doing it per request would kill your API

# from transformers import pipeline
# import sys

# print("🔄 Loading AI models... (this takes 30-60 seconds first time)")

# # ─────────────────────────────────────────────
# # MODEL 1: SENTIMENT ANALYSIS
# # What it does: Determines if text is POSITIVE or NEGATIVE
# # Business use: Customer review analysis, social media monitoring
# # Model: DistilBERT fine-tuned on Stanford Sentiment Treebank
# # ─────────────────────────────────────────────
# try:
#     sentiment_analyzer = pipeline(
#         "sentiment-analysis",
#         model="distilbert-base-uncased-finetuned-sst-2-english",
#         truncation=True,      # cut text if too long
#         max_length=512        # model's max input size
#     )
#     print("✅ Sentiment model loaded")
# except Exception as e:
#     sentiment_analyzer = None
#     print(f"⚠️ Sentiment model failed: {e}")


# # ─────────────────────────────────────────────
# # MODEL 2: ZERO-SHOT CLASSIFICATION
# # What it does: Classify text into ANY categories you define
# # Business use: Support ticket routing, content categorization
# # Special: You don't need training data — works on any labels
# # ─────────────────────────────────────────────
# try:
#     zero_shot_classifier = pipeline(
#         "zero-shot-classification",
#         model="facebook/bart-large-mnli"
#     )
#     print("✅ Zero-shot classifier loaded")
# except Exception as e:
#     zero_shot_classifier = None
#     print(f"⚠️ Classifier model failed: {e}")


# # ─────────────────────────────────────────────
# # MODEL 3: SUMMARIZATION
# # What it does: Condenses long text into short summary
# # Business use: Meeting notes, document processing, news summaries
# # ─────────────────────────────────────────────
# try:
#     summarizer = pipeline(
#         "summarization",
#         model="facebook/bart-large-cnn",
#         truncation=True
#     )
#     print("✅ Summarizer model loaded")
# except Exception as e:
#     summarizer = None
#     print(f"⚠️ Summarizer model failed: {e}")


# # ─────────────────────────────────────────────
# # INFERENCE FUNCTIONS
# # These are called by the route handlers
# # ─────────────────────────────────────────────

# def analyze_sentiment(text: str) -> dict:
#     """
#     Analyzes sentiment of input text.
#     Returns label (POSITIVE/NEGATIVE) and confidence score.
    
#     Real use case: Analyze 1000 customer reviews automatically
#     """
#     if not sentiment_analyzer:
#         # Graceful fallback — never crash the server
#         return {
#             "label": "POSITIVE",
#             "score": 0.85,
#             "mode": "mock",
#             "note": "Model not loaded — returning mock response"
#         }

#     try:
#         result = sentiment_analyzer(text)[0]
#         return {
#             "label": result["label"],
#             "score": round(result["score"], 4),
#             "confidence_percent": f"{round(result['score'] * 100, 2)}%",
#             "mode": "real"
#         }
#     except Exception as e:
#         return {"error": str(e), "mode": "error"}


# def classify_text(text: str, candidate_labels: list) -> dict:
#     """
#     Zero-shot classification — classify text into custom categories.
    
#     Example:
#         text = "My order hasn't arrived after 2 weeks"
#         labels = ["shipping", "refund", "product quality", "account"]
#         → { "label": "shipping", "score": 0.91 }
    
#     Real use case: Route customer support tickets automatically
#     """
#     if not zero_shot_classifier:
#         # Mock fallback
#         return {
#             "sequence": text,
#             "labels": candidate_labels,
#             "scores": [round(1/len(candidate_labels), 3)] * len(candidate_labels),
#             "top_label": candidate_labels[0],
#             "top_score": round(1/len(candidate_labels), 3),
#             "mode": "mock"
#         }

#     try:
#         result = zero_shot_classifier(text, candidate_labels)
#         return {
#             "sequence": result["sequence"],
#             "labels": result["labels"],
#             "scores": [round(s, 4) for s in result["scores"]],
#             "top_label": result["labels"][0],
#             "top_score": round(result["scores"][0], 4),
#             "mode": "real"
#         }
#     except Exception as e:
#         return {"error": str(e), "mode": "error"}


# def summarize_text(text: str, max_length: int = 150, min_length: int = 30) -> dict:
#     """
#     Summarizes long text into a concise version.
    
#     Real use case: Summarize legal documents, meeting transcripts, news articles
#     """
#     if not summarizer:
#         return {
#             "original_length": len(text.split()),
#             "summary": f"[MOCK SUMMARY] This text discusses: {text[:100]}...",
#             "summary_length": 20,
#             "compression_ratio": "mock",
#             "mode": "mock"
#         }

#     try:
#         # BART needs at least 100 words to summarize well
#         word_count = len(text.split())
#         if word_count < 50:
#             return {
#                 "error": "Text too short to summarize. Provide at least 50 words.",
#                 "word_count": word_count
#             }

#         result = summarizer(
#             text,
#             max_length=max_length,
#             min_length=min_length,
#             do_sample=False   # deterministic output (same input = same output)
#         )[0]

#         summary = result["summary_text"]
#         return {
#             "original_word_count": word_count,
#             "summary": summary,
#             "summary_word_count": len(summary.split()),
#             "compression_ratio": f"{round((1 - len(summary.split())/word_count)*100)}% reduction",
#             "mode": "real"
#         }
#     except Exception as e:
#         return {"error": str(e), "mode": "error"}


# def batch_sentiment_analysis(texts: list) -> list:
#     """
#     Analyze sentiment for multiple texts at once.
    
#     Real use case: Process 500 product reviews in one API call
#     More efficient than calling one by one.
#     """
#     if not sentiment_analyzer:
#         return [
#             {
#                 "text": t[:50] + "...",
#                 "label": "POSITIVE",
#                 "score": 0.85,
#                 "mode": "mock"
#             }
#             for t in texts
#         ]

#     try:
#         results = sentiment_analyzer(texts)
#         return [
#             {
#                 "text": texts[i][:80] + ("..." if len(texts[i]) > 80 else ""),
#                 "label": r["label"],
#                 "score": round(r["score"], 4),
#                 "confidence_percent": f"{round(r['score'] * 100, 2)}%"
#             }
#             for i, r in enumerate(results)
#         ]
#     except Exception as e:
#         return [{"error": str(e)}]


# models/ai_pipeline.py
# ============================================================
# CENTRAL AI PIPELINE
# ============================================================
# This file is responsible for:
#
# 1. Loading all AI models ONCE at startup
# 2. Providing reusable inference functions
# 3. Preventing model reload on every API request
#
# WHY THIS MATTERS:
# ------------------------------------------------------------
# Loading transformer models is VERY expensive.
#
# Bad approach:
#   Load model inside every route request ❌
#
# Good approach:
#   Load once when server starts ✅
#
# Real companies ALWAYS preload ML models like this.
#
# ============================================================

from transformers import pipeline
import sys

print("🔄 Loading AI models... (first startup may take 1-5 minutes)")


# ============================================================
# MODEL 1 — SENTIMENT ANALYSIS
# ============================================================
#
# PURPOSE:
# Detect whether text sentiment is:
#   - POSITIVE
#   - NEGATIVE
#
# REAL BUSINESS USE CASES:
# ------------------------------------------------------------
# - Customer review analysis
# - Social media monitoring
# - Product feedback analysis
# - Brand reputation tracking
#
# MODEL:
# DistilBERT fine-tuned on SST-2 dataset
#
# WHY DISTILBERT?
# ------------------------------------------------------------
# - Smaller and faster than BERT
# - Great for laptops
# - Still highly accurate
#
# ============================================================

try:
    sentiment_analyzer = pipeline(
        task="sentiment-analysis",

        # Lightweight sentiment model
        model="distilbert-base-uncased-finetuned-sst-2-english",

        # If text is too long, cut extra tokens
        truncation=True,

        # Maximum tokens model can process
        max_length=512
    )

    print("✅ Sentiment model loaded successfully")

except Exception as e:

    # NEVER crash the entire server if model fails
    sentiment_analyzer = None

    print(f"⚠️ Sentiment model failed: {e}")


# ============================================================
# MODEL 2 — ZERO-SHOT CLASSIFICATION
# ============================================================
#
# PURPOSE:
# Classify text into ANY labels dynamically.
#
# EXAMPLE:
# ------------------------------------------------------------
# Text:
#   "My order still hasn't arrived"
#
# Labels:
#   ["shipping", "refund", "technical issue"]
#
# Output:
#   shipping ✅
#
# SPECIAL FEATURE:
# ------------------------------------------------------------
# No training needed.
#
# You provide labels dynamically at runtime.
#
# REAL BUSINESS USE CASES:
# ------------------------------------------------------------
# - Support ticket routing
# - Email categorization
# - Content moderation
# - Document classification
#
# USING LIGHTWEIGHT MODEL:
# ------------------------------------------------------------
# Original:
#   facebook/bart-large-mnli (~1.6 GB)
#
# Replaced with:
#   valhalla/distilbart-mnli-12-1
#
# Faster and more beginner-laptop friendly.
#
# ============================================================

try:
    zero_shot_classifier = pipeline(
        task="zero-shot-classification",

        # Smaller + faster model
        model="valhalla/distilbart-mnli-12-1"
    )

    print("✅ Zero-shot classifier loaded successfully")

except Exception as e:

    zero_shot_classifier = None

    print(f"⚠️ Zero-shot classifier failed: {e}")


# ============================================================
# MODEL 3 — TEXT SUMMARIZATION
# ============================================================
#
# PURPOSE:
# Convert long text into short summaries.
#
# REAL BUSINESS USE CASES:
# ------------------------------------------------------------
# - Meeting notes summarization
# - Legal document summarization
# - News summarization
# - Research paper summaries
#
# LIGHTWEIGHT VERSION:
# ------------------------------------------------------------
# Original:
#   facebook/bart-large-cnn
#
# Replaced with:
#   sshleifer/distilbart-cnn-12-6
#
# Much smaller and faster.
#
# ============================================================

try:
    summarizer = pipeline(
        task="summarization",

        # Lightweight summarization model
        model="sshleifer/distilbart-cnn-12-6",

        truncation=True
    )

    print("✅ Summarizer model loaded successfully")

except Exception as e:

    summarizer = None

    print(f"⚠️ Summarizer model failed: {e}")


# ============================================================
# ALL MODELS LOADED
# ============================================================

print("🚀 AI Pipeline Ready")
print("-" * 50)


# ============================================================
# INFERENCE FUNCTIONS
# ============================================================
#
# These functions are called from Flask route handlers.
#
# Example flow:
#
# Client Request
#       ↓
# Flask Route
#       ↓
# AI Function
#       ↓
# Model Prediction
#       ↓
# JSON Response
#
# ============================================================


# ============================================================
# FUNCTION 1 — ANALYZE SENTIMENT
# ============================================================

def analyze_sentiment(text: str) -> dict:
    """
    Analyze sentiment of input text.

    INPUT:
        "I love this product"

    OUTPUT:
        {
            "label": "POSITIVE",
            "score": 0.998
        }

    """

    # --------------------------------------------------------
    # FALLBACK MODE
    # --------------------------------------------------------
    # If model failed to load,
    # return mock data instead of crashing API.
    # --------------------------------------------------------

    if not sentiment_analyzer:

        return {
            "label": "POSITIVE",
            "score": 0.85,
            "mode": "mock",
            "note": "Model unavailable — returning mock response"
        }

    try:

        # Run model inference
        result = sentiment_analyzer(text)[0]

        return {
            "label": result["label"],

            # Round score for cleaner API response
            "score": round(result["score"], 4),

            # Human-friendly confidence
            "confidence_percent":
                f"{round(result['score'] * 100, 2)}%",

            "mode": "real"
        }

    except Exception as e:

        return {
            "error": str(e),
            "mode": "error"
        }


# ============================================================
# FUNCTION 2 — ZERO-SHOT CLASSIFICATION
# ============================================================

def classify_text(text: str, candidate_labels: list) -> dict:
    """
    Dynamically classify text into categories.

    EXAMPLE:
    --------------------------------------------------------

    Text:
        "I want refund for damaged product"

    Labels:
        ["refund", "shipping", "technical issue"]

    Output:
        refund

    """

    # --------------------------------------------------------
    # MOCK FALLBACK
    # --------------------------------------------------------

    if not zero_shot_classifier:

        return {
            "sequence": text,

            "labels": candidate_labels,

            # Equal fake scores
            "scores":
                [round(1 / len(candidate_labels), 3)]
                * len(candidate_labels),

            "top_label": candidate_labels[0],

            "top_score":
                round(1 / len(candidate_labels), 3),

            "mode": "mock"
        }

    try:

        # Perform classification
        result = zero_shot_classifier(
            text,
            candidate_labels
        )

        return {

            "sequence": result["sequence"],

            "labels": result["labels"],

            "scores":
                [round(score, 4)
                 for score in result["scores"]],

            # Highest confidence label
            "top_label": result["labels"][0],

            "top_score":
                round(result["scores"][0], 4),

            "mode": "real"
        }

    except Exception as e:

        return {
            "error": str(e),
            "mode": "error"
        }


# ============================================================
# FUNCTION 3 — TEXT SUMMARIZATION
# ============================================================

def summarize_text(
    text: str,
    max_length: int = 150,
    min_length: int = 30
) -> dict:
    """
    Summarize long text.

    WHY min_length / max_length?
    --------------------------------------------------------
    Controls summary size.

    Example:
        max_length=150
        → summary won't exceed ~150 tokens

    """

    # --------------------------------------------------------
    # MOCK FALLBACK
    # --------------------------------------------------------

    if not summarizer:

        return {
            "original_length": len(text.split()),

            "summary":
                f"[MOCK SUMMARY] {text[:100]}...",

            "summary_length": 20,

            "compression_ratio": "mock",

            "mode": "mock"
        }

    try:

        # Count input words
        word_count = len(text.split())

        # Summarizers work badly on tiny text
        if word_count < 50:

            return {
                "error":
                    "Text too short. "
                    "Provide at least 50 words.",

                "word_count": word_count
            }

        # ----------------------------------------------------
        # RUN SUMMARIZATION MODEL
        # ----------------------------------------------------

        result = summarizer(
            text,

            max_length=max_length,

            min_length=min_length,

            # Same input = same output
            do_sample=False
        )[0]

        summary = result["summary_text"]

        return {

            "original_word_count": word_count,

            "summary": summary,

            "summary_word_count":
                len(summary.split()),

            "compression_ratio":
                f"{round((1 - len(summary.split()) / word_count) * 100)}% reduction",

            "mode": "real"
        }

    except Exception as e:

        return {
            "error": str(e),
            "mode": "error"
        }


# ============================================================
# FUNCTION 4 — BATCH SENTIMENT ANALYSIS
# ============================================================
#
# WHY BATCH PROCESSING?
# ------------------------------------------------------------
# Running predictions in batches is MUCH faster
# than processing one-by-one.
#
# Real companies process:
# - thousands of reviews
# - tweets
# - support messages
#
# in batches.
#
# ============================================================

def batch_sentiment_analysis(texts: list) -> list:

    # --------------------------------------------------------
    # MOCK FALLBACK
    # --------------------------------------------------------

    if not sentiment_analyzer:

        return [

            {
                "text": text[:50] + "...",

                "label": "POSITIVE",

                "score": 0.85,

                "mode": "mock"
            }

            for text in texts
        ]

    try:

        # Batch inference
        results = sentiment_analyzer(texts)

        formatted_results = []

        # Combine original text + prediction
        for i, result in enumerate(results):

            formatted_results.append({

                "text":
                    texts[i][:80]
                    + ("..." if len(texts[i]) > 80 else ""),

                "label": result["label"],

                "score": round(result["score"], 4),

                "confidence_percent":
                    f"{round(result['score'] * 100, 2)}%"
            })

        return formatted_results

    except Exception as e:

        return [
            {
                "error": str(e)
            }
        ]