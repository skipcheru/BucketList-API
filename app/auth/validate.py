from flask_jwt import JWT
from functools import wraps
from werkzeug.exceptions import BadRequest
from flask import request, jsonify, Blueprint, abort

jwt = JWT()


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
                    if (argument not in data or not data.get(argument) or
                            data.get(argument).isspace()):
                        msg = 'username and password required'
                        return jsonify({'error': msg}), 400
            except BadRequest:
                msg = "Request must have valid data"
                return jsonify({"error": msg}), 400
            return f(*args, **kwargs)
        return decorated_function
    return wrapper

from app.models import User


@jwt.authentication_handler
def authenticate(username, password):
    user = User.query.filter_by(username=username).scalar()
    if user and user.verify_password(password):
        return user


@jwt.identity_handler
def identity(payload):
    user_id = payload['identity']
    return User.query.filter(user_id == User.id).scalar()
