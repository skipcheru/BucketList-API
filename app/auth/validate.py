from functools import wraps
from werkzeug.exceptions import BadRequest
from flask import request, jsonify, Blueprint, abort


# Validate all requests
def validate_json(*expected_args):
    def wrapper(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not request.is_json:
                msg = "Request must be a valid json"
                return jsonify({"error": msg}), 415
            try:
                data = request.get_json()
                for argument in expected_args:
                    if (not data.get(argument) or data.get(argument).isspace()):
                        msg = argument + ' required'
                        return jsonify({'error': msg}), 400
            except BadRequest:
                msg = "Request must have valid data"
                return jsonify({"error": msg}), 400
            return f(*args, **kwargs)
        return decorated_function
    return wrapper
