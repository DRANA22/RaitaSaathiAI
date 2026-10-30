from flask import jsonify

def api_response(success=True, data=None, error=None, status_code=200, metadata=None):
    """Standardized JSON response envelope across the RaitaSaathiAI API."""
    payload = {
        "success": success,
        "data": data if data is not None else {},
        "error": error,
        "metadata": metadata if metadata is not None else {
            "platform": "RaitaSaathiAI",
            "version": "1.0.0"
        }
    }
    return jsonify(payload), status_code

def bad_request(message, code="BAD_REQUEST"):
    return api_response(
        success=False, 
        error={"code": code, "message": message}, 
        status_code=400
    )

def unauthorized(message="Authentication required.", code="UNAUTHORIZED"):
    return api_response(
        success=False, 
        error={"code": code, "message": message}, 
        status_code=401
    )

def forbidden(message="Access denied to requested resource.", code="FORBIDDEN"):
    return api_response(
        success=False, 
        error={"code": code, "message": message}, 
        status_code=403
    )

def not_found(message="Requested resource not found.", code="NOT_FOUND"):
    return api_response(
        success=False, 
        error={"code": code, "message": message}, 
        status_code=404
    )

def internal_error(message="An unexpected server error occurred.", code="INTERNAL_SERVER_ERROR"):
    return api_response(
        success=False, 
        error={"code": code, "message": message}, 
        status_code=500
    )

