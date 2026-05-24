# utils/response_helper.py
# Standardized API responses — consistency across all endpoints
# In real companies, ALL endpoints return the same shape
# Frontend devs love this because they know exactly what to expect

from datetime import datetime

def success_response(data, message="Success", status_code=200):
    """Standard success response wrapper"""
    return {
        "success": True,
        "message": message,
        "data": data,
        "timestamp": datetime.utcnow().isoformat(),
        "status_code": status_code
    }, status_code


def error_response(message, status_code=400, details=None):
    """Standard error response wrapper"""
    response = {
        "success": False,
        "message": message,
        "timestamp": datetime.utcnow().isoformat(),
        "status_code": status_code
    }
    if details:
        response["details"] = details
    return response, status_code


def validation_error(field, message):
    """Specific validation error"""
    return error_response(
        message=f"Validation failed: {message}",
        status_code=422,
        details={"field": field, "issue": message}
    )