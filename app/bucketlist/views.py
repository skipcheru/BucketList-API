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
    search = request.args.get('q', '')
    page = request.args.get('page', 1)
    limit = request.args.get('limit', 20)

    results = BucketList.query.filter_by(user_id=current_identity.id).filter(
        BucketList.name.ilike(f'%{search}%')).paginate(int(page), int(limit), False)
    if not results:
        return jsonify({"error": "BucketList not found"}), 404

    buckets = [bucket.to_json() for bucket in results.items]

    return jsonify(buckets), 200


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
    return any_request(request.method, BucketList, bucket_id, data)


@bucketlists.route('/<int:bucket_id>', methods=['GET', 'DELETE'])
@jwt_required()
def bucketlist(bucket_id):
    return any_request(request.method, BucketList, bucket_id, None)


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
    return any_request(request.method, Item, item_id, data)


@bucketlists.route('/<int:bucket_id>/items/<int:item_id>',
                   methods=['GET', 'DELETE'])
@jwt_required()
def modify_bucketlist_item(bucket_id, item_id):
    return any_request(request.method, Item, item_id, None)


# use this to carry out GET, PUT, DELETE
def any_request(method, model, model_id, data):

    model_obj = model.query.filter_by(id=model_id).first()

    if not model_obj:
        return jsonify({'error': model().__class__.__name__ +
                        ' not found'}), 404

    if method == 'GET':
        return jsonify(model_obj.to_json()), 200

    elif method == 'PUT':
        model_obj.name = data['name']
        db.session.commit()
        return jsonify({'message': model().__class__.__name__ +
                        ' updated successfully'}), 200

    elif method == 'DELETE':
        db.session.delete(model_obj)
        db.session.commit()
        return jsonify({'message': model().__class__.__name__ +
                        ' deleted successfully'}), 200
