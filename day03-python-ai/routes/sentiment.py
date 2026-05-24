# routes/sentiment.py
# Sentiment analysis endpoints

from flask import Blueprint, request, jsonify
from models.ai_pipeline import analyze_sentiment, batch_sentiment_analysis
from middleware.validator import validate_text_input
from utils.response_helper import success_response, error_response

sentiment_bp = Blueprint("sentiment", __name__)


@sentiment_bp.route("/analyze", methods=["POST"])
def analyze():
    """
    POST /api/sentiment/analyze
    Analyzes sentiment of a single text.
    
    Request body:
    {
        "text": "I love this product, it works amazing!"
    }
    
    Response:
    {
        "success": true,
        "data": {
            "label": "POSITIVE",
            "score": 0.9998,
            "confidence_percent": "99.98%"
        }
    }
    """
    data = request.get_json()
    text, err = validate_text_input(data, field="text", min_length=3, max_length=1000)
    if err:
        return jsonify(err[0]), err[1]

    result = analyze_sentiment(text)

    if "error" in result:
        return jsonify(error_response("AI processing failed", 500, result["error"])[0]), 500

    return jsonify(success_response(
        data={
            "input_text": text[:100] + ("..." if len(text) > 100 else ""),
            "analysis": result
        },
        message="Sentiment analysis complete"
    )[0])


@sentiment_bp.route("/batch", methods=["POST"])
def batch_analyze():
    """
    POST /api/sentiment/batch
    Analyze sentiment for multiple texts at once.
    
    Real use case: Process all customer reviews for a product.
    
    Request body:
    {
        "texts": [
            "Great product!",
            "Terrible experience, never buying again.",
            "It was okay, nothing special."
        ]
    }
    """
    data = request.get_json()

    if not data or "texts" not in data:
        return jsonify(error_response("'texts' array is required")[0]), 400

    texts = data.get("texts")

    if not isinstance(texts, list) or len(texts) == 0:
        return jsonify(error_response("'texts' must be a non-empty array")[0]), 400

    if len(texts) > 20:
        return jsonify(error_response("Max 20 texts per batch request")[0]), 400

    # Validate each text
    for i, t in enumerate(texts):
        if not isinstance(t, str) or len(t.strip()) < 3:
            return jsonify(error_response(f"Text at index {i} is invalid or too short")[0]), 422

    results = batch_sentiment_analysis(texts)

    # Calculate summary statistics
    positives = sum(1 for r in results if r.get("label") == "POSITIVE")
    negatives = len(results) - positives

    return jsonify(success_response(
        data={
            "total_analyzed": len(results),
            "summary": {
                "positive_count": positives,
                "negative_count": negatives,
                "positive_percent": f"{round(positives/len(results)*100)}%",
                "negative_percent": f"{round(negatives/len(results)*100)}%"
            },
            "results": results
        },
        message="Batch sentiment analysis complete"
    )[0])