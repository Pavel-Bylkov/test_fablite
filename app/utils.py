from flask import request, jsonify
from functools import wraps

def validate_json(*expected_args):
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            data = request.get_json()
            if not data:
                return jsonify({"error": "Invalid JSON"}), 400
            for arg in expected_args:
                if arg not in data:
                    return jsonify({"error": f"Missing argument: {arg}"}), 400
            return f(*args, **kwargs)
        return wrapper
    return decorator