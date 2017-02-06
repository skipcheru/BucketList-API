from app.models import User, BucketList, Item
from flask import request, jsonify, Blueprint
from app import db, jwt
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
        return jsonify({"error": "Page  and limit should be Integers"}), 400

    results = BucketList.query.filter_by(user_id=current_identity.id).filter(
        BucketList.name.ilike(f'%{search}%')).paginate(page, limit, False)

    if not results:
        return jsonify({"error": "BucketList not found"}), 404

    buckets = [bucket.to_json() for bucket in results.items]

    return jsonify(buckets), 200


# Add new bucketlist
@bucketlists.route('/', methods=['POST'])
@jwt_required()
@validate_json('name', 'description')
def new_bucketlist():
    data = request.get_json()
    return post_request(BucketList, None, data)


# Update single bucketlist
@bucketlists.route('/<int:bucket_id>', methods=['PUT'])
@jwt_required()
def update_bucketlist(bucket_id):
    return put_request(BucketList, request, bucket_id, None)


# Get and Delete single bucketlist
@bucketlists.route('/<int:bucket_id>', methods=['GET', 'DELETE'])
@jwt_required()
def bucketlist(bucket_id):
    return any_request(request.method, BucketList, bucket_id)


# Get all bucketlist items
@bucketlists.route('/<int:bucket_id>/items/', methods=['GET'])
@jwt_required()
def get_bucketlist_item(bucket_id):
    all_items = [item.to_json() for item in
                 Item.query.filter_by(bucket_id=bucket_id).all()]
    return jsonify(all_items), 200


# Create new  bucketlist item
@bucketlists.route('/<int:bucket_id>/items/', methods=['POST'])
@jwt_required()
@validate_json('name')
def new_bucketlist_item(bucket_id):
    data = request.get_json()
    return post_request(Item, bucket_id, data)


# Update bucketlist item
@bucketlists.route('/<int:bucket_id>/items/<int:item_id>', methods=['PUT'])
@jwt_required()
def update_bucketlist_item(item_id, bucket_id):
    return put_request(Item, request, bucket_id, item_id)


# Get and Delete bucketlist item
@bucketlists.route('/<int:bucket_id>/items/<int:item_id>',
                   methods=['GET', 'DELETE'])
@jwt_required()
def modify_bucketlist_item(bucket_id, item_id):
    return any_request(request.method, Item, bucket_id, item_id)


# use this to carry out GET, DELETE
def any_request(method, model, bucket_id=None, item_id=None, data=None):
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


# use this to carry out PUT request only
def put_request(model, request, bucket_id, item_id):
    user_id = current_identity.id

    if not request.is_json:
        return jsonify({"error": 'Request must be a valid json'}), 415

    if model == BucketList:
        model_obj = model.query.filter_by(
            user_id=user_id, id=bucket_id).first()
    else:
        model_obj = model.query.filter_by(
            bucket_id=bucket_id, id=item_id).filter(User.id == user_id).first()

    if not model_obj:
        return jsonify({'error': model().__class__.__name__ + ' not found'}), 404

    response = jsonify({'message': model().__class__.__name__ +
                        ' updated successfully'}), 200

    data = request.get_json()
    description = data.get('description', None)
    status = data.get('status', None)
    name = data.get('name', None)

    if name and name.isspace():
        return jsonify({'error': 'name missing from request'}), 400

    if description and description.isspace():
        return jsonify({'error': 'description missing from request'}), 400

    if status and status.lower() not in ('true', 'false'):
        return jsonify({'error': 'Status should be either true or false'}), 400

    if model == BucketList:
        model_obj.description = description or model_obj.description
        model_obj.name = name or model_obj.name

    else:
        done = True if status == 'true' else False
        model_obj.done = done
        model_obj.name = name or model_obj.name

    db.session.commit()
    return response


# use this to carry out POST request only
def post_request(model, bucket_id, data):
    user_id, name = current_identity.id, data['name']

    if model == BucketList:
        model_obj = model.query.filter_by(user_id=user_id, name=name).first()
        description = data['description']

    else:
        model_obj = model.query.filter_by(
            bucket_id=bucket_id, name=name).filter(User.id == user_id).first()

    if model_obj:
        return jsonify({'error': model().__class__.__name__ +
                        ' already exists'}), 409

    if model == BucketList:
        model_obj = model(name=name, description=description, user_id=user_id)

    else:
        model_obj = model(name=name, bucket_id=bucket_id)

    db.session.add(model_obj)
    db.session.commit()
    return jsonify({'message': model().__class__.__name__ +
                    ' added successfully'}), 201
