# routes/classifier.py

# Import Flask tools
from flask import Blueprint, request, jsonify

# Import AI function
from models.ai_pipeline import classify_text

# Import validation functions
from middleware.validator import validate_text_input, validate_labels

# Import response helper
from utils.response_helper import success_response, error_response


# Create Blueprint
classifier_bp = Blueprint("classifier", __name__)


# Ready-made label groups
PRESET_LABELS = {
    "support": [
        "billing",
        "technical issue",
        "shipping",
        "refund",
        "account"
    ],

    "priority": [
        "urgent",
        "high",
        "medium",
        "low"
    ],

    "emotion": [
        "happy",
        "sad",
        "angry",
        "neutral"
    ]
}


# POST /api/classifier/classify
@classifier_bp.route("/classify", methods=["POST"])
def classify():

    # Get JSON data
    data = request.get_json()


    # Validate text input
    text, err = validate_text_input(data)

    if err:
        return jsonify(err[0]), err[1]


    # Check preset labels
    preset = data.get("preset")


    # If preset exists
    if preset:

        # Invalid preset
        if preset not in PRESET_LABELS:

            return jsonify(
                error_response("Invalid preset")[0]
            ), 400

        # Use preset labels
        labels = PRESET_LABELS[preset]

    else:

        # Use custom labels
        labels, err = validate_labels(data)

        if err:
            return jsonify(err[0]), err[1]


    # Run AI classification
    result = classify_text(text, labels)


    # AI error
    if "error" in result:

        return jsonify(
            error_response("Classification failed")[0]
        ), 500


    # Success response
    return jsonify(

        success_response(

            data={
                "input_text": text,
                "classification": result,
                "preset_used": preset
            },

            message="Classification complete"

        )[0]

    )


# GET /api/classifier/presets
@classifier_bp.route("/presets", methods=["GET"])
def get_presets():

    return jsonify(

        success_response(

            data={
                "presets": PRESET_LABELS
            },

            message="Available presets"

        )[0]

    )