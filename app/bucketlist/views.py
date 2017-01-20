from app.models import User, BucketList, Item
from flask import request, jsonify, Blueprint
from app import db

bucketlists = Blueprint('bucketlists', __name__, url_prefix='/bucketlists')


@bucketlists.route('/', methods=['GET', 'POST'])
def new_bucketlist():
    pass


@bucketlists.route('/<id>', methods=['GET', 'PUT', 'DELETE'])
def bucketlist():
    pass


@bucketlists.route('/<id>/items/', methods=['GET', 'POST'])
def bucketlist_item():
    pass


@bucketlists.route('/bucketlists/<id>/items/<item_id>',
                   methods=['GET', 'PUT', 'DELETE'])
def modify_bucketlist_item():
    pass
