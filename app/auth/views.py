# from app.models import User
from flask import request, jsonify, Blueprint, abort, make_response
from app import db, jwt
from app.models import User


auth = Blueprint('auth', __name__, url_prefix='/api/v1/auth')

from .validate import validate_json, authenticate, identity


# Authenticate user
@auth.route('/login', methods=['POST'])
@validate_json('username', 'password')
def login():
    data = request.get_json()

    identity = jwt.authentication_callback(data['username'], data['password'])
    if identity:
        access_token = jwt.jwt_encode_callback(identity)
        return jwt.auth_response_callback(access_token, identity)

    return jsonify({'message': 'Invalid credentials'}), 401


# Register user
@auth.route('/register', methods=['POST'])
@validate_json('username', 'password')
def register():
    data = request.get_json()
    username, password = data['username'], data['password']
    user = User.query.filter_by(username=username).first()
    if user:
        return jsonify({'error': 'User already exists'}), 409

    user = User(username=username, password=password)
    db.session.add(user)
    db.session.commit()
    return jsonify({'message': 'User registered successfully'}), 201
