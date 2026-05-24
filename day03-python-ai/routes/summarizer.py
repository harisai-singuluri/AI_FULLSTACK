# routes/summarizer.py
# Text summarization endpoint

from flask import Blueprint, request, jsonify
from models.ai_pipeline import summarize_text
from middleware.validator import validate_text_input
from utils.response_helper import success_response, error_response

summarizer_bp = Blueprint("summarizer", __name__)


@summarizer_bp.route("/summarize", methods=["POST"])
def summarize():
    """
    POST /api/summarizer/summarize
    Summarizes a long piece of text.
    
    Request body:
    {
        "text": "Long article or document text here...",
        "max_length": 150,
        "min_length": 30
    }
    
    Real use case: Summarize customer complaint emails,
    legal documents, meeting transcripts automatically.
    """
    data = request.get_json()

    # Allow up to 5000 chars for summarization
    text, err = validate_text_input(data, field="text", min_length=50, max_length=5000)
    if err:
        return jsonify(err[0]), err[1]

    max_length = data.get("max_length", 150)
    min_length = data.get("min_length", 30)

    # Validate length params
    if not isinstance(max_length, int) or max_length < 30 or max_length > 500:
        return jsonify(error_response("max_length must be integer between 30-500")[0]), 400

    if not isinstance(min_length, int) or min_length < 10 or min_length >= max_length:
        return jsonify(error_response("min_length must be integer less than max_length")[0]), 400

    result = summarize_text(text, max_length=max_length, min_length=min_length)

    if "error" in result:
        return jsonify(error_response(result["error"], 400)[0]), 400

    return jsonify(success_response(
        data=result,
        message="Summarization complete"
    )[0])