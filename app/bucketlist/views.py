from app.models import User, BucketList, Item
from flask import request, jsonify, Blueprint
from app import db, jwt
from flask_jwt import jwt_required, current_identity
from app.auth.validate import validate_json


bucketlists = Blueprint('bucketlists', __name__,
                        url_prefix='/api/v1/bucketlists')


# get method for all bucketlists and search bucketlists
@bucketlists.route('/', methods=['GET'])
@jwt_required()
def get_bucketlist():
    query = request.args.get('q')
    if query:
        bucket = BucketList.query.filter_by(name=query).first()
        if bucket:
            return jsonify(bucket.to_json())
        return jsonify({"error": "BucketList not found"}), 404

    all_buckets = [bucket.to_json() for bucket in BucketList.query.all()]
    return jsonify(all_buckets)


# add new bucketlist here
@bucketlists.route('/', methods=['POST'])
@jwt_required()
@validate_json('name')
def new_bucketlist():
    data = request.get_json()
    bucket = BucketList.query.filter_by(name=data['name']).first()
    if bucket:
        return jsonify({'error': 'BucketList already exists'}), 409

    bucket = BucketList(name=data['name'], user_id=current_identity.id)
    db.session.add(bucket)
    db.session.commit()
    return jsonify({'message': 'BucketList added successfully'}), 201


@bucketlists.route('/<int:bucket_id>', methods=['PUT'])
@jwt_required()
@validate_json('name')
def update_bucketlist(bucket_id):
    data = request.get_json()
    bucket = BucketList.query.filter_by(id=bucket_id).first()
    if bucket:
        bucket.name = data['name']
        db.session.commit()
        return jsonify({'message': 'BucketList updated successfully'}), 201

    return jsonify({'error': 'BucketList not Found'}), 404


@bucketlists.route('/<int:bucket_id>', methods=['GET', 'DELETE'])
@jwt_required()
def bucketlist(bucket_id):
    return any_request(request.method, BucketList, bucket_id)


@bucketlists.route('/<int:bucket_id>/items/', methods=['GET'])
@jwt_required()
def get_bucketlist_item(bucket_id):
    all_items = [item.to_json() for item in
                 Item.query.filter_by(bucket_id=bucket_id).all()]
    return jsonify(all_items), 200


@bucketlists.route('/<int:bucket_id>/items/', methods=['POST'])
@jwt_required()
@validate_json('name')
def new_bucketlist_item(bucket_id):
    data = request.get_json()
    item = Item.query.filter_by(name=data['name']).first()
    if item:
        return jsonify({'error': 'Item already exists'}), 409

    item = Item(name=data['name'], bucket_id=bucket_id)
    db.session.add(item)
    db.session.commit()
    return jsonify({'message': 'Bucketlist item added'}), 201


@bucketlists.route('/<int:bucket_id>/items/<int:item_id>', methods=['PUT'])
@jwt_required()
@validate_json('name')
def update_bucketlist_item(item_id, bucket_id):
    data = request.get_json()
    item = Item.query.filter_by(id=item_id).first()
    if item:
        item.name = data['name']
        db.session.commit()
        return jsonify({'message': 'Item updated successfully'}), 201

    return jsonify({'error': 'BucketList not Found'}), 404


@bucketlists.route('/<int:bucket_id>/items/<int:item_id>',
                   methods=['GET', 'DELETE'])
@jwt_required()
def modify_bucketlist_item(bucket_id, item_id):
    return any_request(request.method, Item, item_id)


# use this to carry out DELETE OR GET
def any_request(method, model, model_id):
    model_obj = model.query.filter_by(id=model_id).first()
    if not model_obj:
        return jsonify({'error': model().__class__.__name__ + ' not Found'}), 404

    if method == 'GET':
        return jsonify(model_obj.to_json()), 200

    elif method == 'DELETE':
        db.session.delete(model_obj)
        db.session.commit()
        return jsonify({'message': model().__class__.__name__ + ' deleted successfully'}), 200
