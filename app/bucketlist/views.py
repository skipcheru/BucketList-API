from app.models import User, BucketList, Item
from flask import request, jsonify, Blueprint
from app import db
from flask_jwt import jwt_required, current_identity
from app.auth.validate import validate_json
from sqlalchemy.sql import func


bucketlists = Blueprint('bucketlists', __name__,
                        url_prefix='/api/v1/bucketlists')


# Get all bucketlists and search bucketlists
@bucketlists.route('/', methods=['GET'])
@jwt_required()
def get_bucketlist():
    search = request.args.get('q', '')
    page = request.args.get('page', 1)
    limit = request.args.get('limit', 20)
    try:
        page, limit = int(page), int(limit)
    except ValueError as e:
        return jsonify({"error": "Page and limit should be Integers"}), 400

    results = BucketList.query.filter_by(user_id=current_identity.id).filter(
        BucketList.name.ilike(f'%{search}%')).paginate(page, limit, False)

    buckets = [bucket.to_json() for bucket in results.items]
    count = len(buckets)

    if not buckets and search:
        return jsonify({"error": "BucketList not found"}), 404

    return jsonify({"count": count, "buckets": buckets}), 200


# Add new bucketlist
@bucketlists.route('/', methods=['POST'])
@jwt_required()
@validate_json('name', 'description')
def new_bucketlist():
    data, user_id = request.get_json(), current_identity.id
    bucket = BucketList.query.filter_by(
        user_id=user_id, name=data['name']).first()

    if bucket:
        return jsonify({'error': 'BucketList already exists'}), 409

    bucketlist = BucketList(
        name=data['name'], description=data['description'], user_id=user_id)

    db.session.add(bucketlist)
    db.session.commit()
    return jsonify(bucketlist.to_json()), 201


# Update single bucketlist
@bucketlists.route('/<int:bucket_id>', methods=['PUT'])
@jwt_required()
def update_bucketlist(bucket_id):
    user_id = current_identity.id

    if not request.is_json:
        return jsonify({"error": 'Request must be a valid json'}), 415

    bucket = BucketList.query.filter_by(user_id=user_id, id=bucket_id).first()

    if not bucket:
        return jsonify({'error': 'BucketList not found'}), 404

    data = request.get_json()
    description = data.get('description', None)
    name = data.get('name', None)

    if name and name.isspace():
        return jsonify({'error': 'name missing from request'}), 400

    if description and description.isspace():
        return jsonify({'error': 'description missing from request'}), 400

    bucket.description = description or bucket.description
    bucket.name = name or bucket.name
    db.session.commit()
    return jsonify(bucket.to_json())


# Get and Delete single bucketlist
@bucketlists.route('/<int:bucket_id>', methods=['GET', 'DELETE'])
@jwt_required()
def bucketlist(bucket_id):
    return get_delete_request(request.method, BucketList, bucket_id)


# Get all bucketlist items
@bucketlists.route('/<int:bucket_id>/items/', methods=['GET'])
@jwt_required()
def get_bucketlist_item(bucket_id):
    all_items = [item.to_json() for item in
                 Item.query.filter_by(bucket_id=bucket_id).all()]

    count = len(all_items)

    return jsonify({"count": count, "items": all_items}), 200


# Create new  bucketlist item
@bucketlists.route('/<int:bucket_id>/items/', methods=['POST'])
@jwt_required()
@validate_json('name')
def new_bucketlist_item(bucket_id):
    data, user_id = request.get_json(), current_identity.id
    item = Item.query.filter_by(bucket_id=bucket_id, name=data['name']).first()

    if item:
        return jsonify({'error': 'Item already exists'}), 409

    bucketitem = Item(name=data['name'],  bucket_id=bucket_id)

    db.session.add(bucketitem)
    db.session.commit()
    return jsonify(bucketitem.to_json()), 201


# Update bucketlist item
@bucketlists.route('/<int:bucket_id>/items/<int:item_id>', methods=['PUT'])
@jwt_required()
def update_bucketlist_item(item_id, bucket_id):
    user_id = current_identity.id

    if not request.is_json:
        return jsonify({"error": 'Request must be a valid json'}), 415

    data = request.get_json()
    status = data.get('status', None)
    name = data.get('name', None)

    if name and name.isspace():
        return jsonify({'error': 'name missing from request'}), 400

    if status and status.lower() not in ('true', 'false'):
        return jsonify({'error': 'Status should be either true or false'}), 400

    item = Item.query.filter_by(
        bucket_id=bucket_id, id=item_id).filter(User.id == user_id).first()

    if not item:
        return jsonify({'error': 'Item not found'}), 404

    done = True if status == 'true' else False
    item.done = done
    item.name = name or item.name

    db.session.commit()
    return jsonify(item.to_json())


# Get and Delete bucketlist item
@bucketlists.route('/<int:bucket_id>/items/<int:item_id>',
                   methods=['GET', 'DELETE'])
@jwt_required()
def modify_bucketlist_item(bucket_id, item_id):
    return get_delete_request(request.method, Item, bucket_id, item_id)


# use this to carry out GET, DELETE
def get_delete_request(method, model, bucket_id=None, item_id=None, data=None):
    user_id = current_identity.id

    if model == BucketList:
        model_obj = model.query.filter_by(
            user_id=user_id, id=bucket_id).first()
    else:
        model_obj = model.query.filter_by(
            bucket_id=bucket_id, id=item_id).filter(User.id == user_id).first()

    if not model_obj:
        return jsonify({'error': model().__class__.__name__ +
                        ' not found'}), 404

    if method == 'GET':
        return jsonify(model_obj.to_json()), 200

    elif method == 'DELETE':
        db.session.delete(model_obj)
        db.session.commit()
        return jsonify({'message': model().__class__.__name__ +
                        ' deleted successfully'}), 200
