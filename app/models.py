from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.sql import func


class User(db.Model):
    """Model for User."""

    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True)
    password = db.Column(db.String(64), unique=True)
    date_created = db.Column(db.DateTime, default=func.now())
    bucket_list = db.relationship(
        'BucketList', backref="bucket", lazy='dynamic', cascade='delete,all')

    def __init__(self, username, password):
        self.username = username
        self.password = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password, password)

    def __repr__(self):
        return '<User %s>' % self.username


class BucketList(db.Model):
    """Model for Bucket."""
    __tablename__ = 'bucketlist'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    description = db.Column(db.String(128))
    items = db.relationship('Item', backref="items",
                            lazy='dynamic', cascade='delete,all')
    date_created = db.Column(db.DateTime, default=func.now())
    date_modified = db.Column(
        db.DateTime, default=func.now(), onupdate=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))

    def __repr__(self):
        return '<BucketList %s>' % self.name

    def to_json(self):

        bucket_json = {
            "Id": self.id,
            "Name": self.name,
            "description": self.description,
            "items": [item.to_json() for item in self.items],
            "date_created": str(self.date_created),
            "date_modified": str(self.date_modified),
            "created_by": self.user_id
        }
        return bucket_json


class Item(db.Model):
    """Modelfor BucketList."""
    __tablename__ = 'item'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    date_created = db.Column(db.DateTime, default=func.now())
    date_modified = db.Column(
        db.DateTime, default=func.now(), onupdate=func.now())
    done = db.Column(db.Boolean, default=False)
    bucket_id = db.Column(db.Integer, db.ForeignKey("bucketlist.id"))

    def __repr__(self):
        return '<Item %s>' % self.name

    def to_json(self):
        item_json = {
            "id": self.id,
            "name": self.name,
            "date_created": str(self.date_created),
            "date_modified": str(self.date_modified),
            "done": self.done
        }
        return item_json
