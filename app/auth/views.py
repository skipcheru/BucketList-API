from flask import request, jsonify, Blueprint, abort, make_response
from app import db
from app.models import User
from app.auth.validate import validate_json
from flask_jwt import JWT
from sqlalchemy import exc


jwt = JWT()
auth = Blueprint('auth', __name__, url_prefix='/api/v1/auth')


# JWT handlers
@jwt.authentication_handler
def authenticate(username, password):
    user = User.query.filter_by(username=username).scalar()
    if user and user.verify_password(password):
        return user


@jwt.identity_handler
def identity(payload):
    user_id = payload['identity']
    return User.query.filter(user_id == User.id).scalar()


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

    try:
        user = User(username=username, password=password)
        db.session.add(user)
        db.session.commit()
        return jsonify({'message': user.username + ' registered successfully'}), 201

    except exc.IntegrityError as e:
        db.session.rollback()
        return jsonify({'error': 'User already exists'}), 409
