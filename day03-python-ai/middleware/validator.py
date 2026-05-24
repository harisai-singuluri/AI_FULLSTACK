# middleware/validator.py
# Input validation functions — ALWAYS validate before processing
# Never trust client input — this is a security rule

from utils.response_helper import validation_error

def validate_text_input(data: dict, field: str = "text", min_length: int = 3, max_length: int = 1000):
    """
    Validates text input from request body.
    Returns (text, None) on success
    Returns (None, error_response) on failure
    """
    if not data:
        return None, validation_error("body", "Request body is empty or not valid JSON")

    text = data.get(field)

    if text is None:
        return None, validation_error(field, f"'{field}' field is required")

    if not isinstance(text, str):
        return None, validation_error(field, f"'{field}' must be a string")

    text = text.strip()

    if len(text) < min_length:
        return None, validation_error(field, f"'{field}' must be at least {min_length} characters")

    if len(text) > max_length:
        return None, validation_error(
            field,
            f"'{field}' exceeds max length of {max_length} characters. Got {len(text)}."
        )

    return text, None


def validate_labels(data: dict, field: str = "labels", min_count: int = 2, max_count: int = 10):
    """
    Validates classification labels list.
    """
    labels = data.get(field)

    if not labels:
        return None, validation_error(field, f"'{field}' is required")

    if not isinstance(labels, list):
        return None, validation_error(field, f"'{field}' must be an array")

    if len(labels) < min_count:
        return None, validation_error(field, f"Provide at least {min_count} labels")

    if len(labels) > max_count:
        return None, validation_error(field, f"Max {max_count} labels allowed")

    # Check all items are strings
    for i, label in enumerate(labels):
        if not isinstance(label, str) or not label.strip():
            return None, validation_error(field, f"Label at index {i} is invalid")

    return [l.strip() for l in labels], None