from app.models import User
from flask import request, jsonify, Blueprint, json
from .. import db

auth = Blueprint('auth', __name__, url_prefix='/auth')


@auth.route('/register', methods=['POST'])
def register():
    return jsonify({'message': 'Register user here'})


@auth.route('/login', methods=['POST'])
def login():
    return jsonify({'message': 'Authenticate user here'})
