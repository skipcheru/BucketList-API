from app.models import User, BucketList, Item
from flask import request, jsonify, Blueprint
from app import db, jwt
from flask_jwt import jwt_required, current_identity


bucketlists = Blueprint('bucketlists', __name__,
                        url_prefix='/api/v1/bucketlists')


@bucketlists.route('/', methods=['GET', 'POST'])
@jwt_required()
def new_bucketlist():
    if request.method == 'POST':
        return jsonify({'message': 'Add bucketlists here'})

    elif request.method == 'GET':
        return jsonify({'message': 'Get all bucketlists here'})


@bucketlists.route('/<int:bucket_id>', methods=['GET', 'PUT', 'DELETE'])
@jwt_required()
def bucketlist(bucket_id):
    if request.method == 'GET':

        return jsonify({'message': 'Get single bucketlist here'})

    elif request.method == 'PUT':
        return jsonify({'message': 'Update bucketlist here'})

    elif request.method == 'DELETE':
        return jsonify({'message': 'Delete bucketlist here'})


@bucketlists.route('/<int:bucket_id>/items/', methods=['GET', 'POST'])
@jwt_required()
def bucketlist_item(bucket_id):
    if request.method == 'POST':
        return jsonify({'message': 'Add bucketlist item here'})

    elif request.method == 'GET':
        return jsonify({'message': 'Get all bucketlist items here'})


@bucketlists.route('/<int:bucket_id>/items/<int:item_id>',
                   methods=['GET', 'PUT', 'DELETE'])
@jwt_required()
def modify_bucketlist_item(bucket_id, item_id):
    if request.method == 'GET':
        return jsonify({'message': 'Get single bucketlist item here'})

    elif request.method == 'PUT':
        return jsonify({'message': 'Update bucketlist item here'})

    elif request.method == 'DELETE':
        return jsonify({'message': 'Delete bucketlist item here'})
