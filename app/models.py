from app import db
from datetime import datetime

class User(db.Model):
    """Model for User."""
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(64), unique=True)
    password = db.Column(db.String(64), unique=True)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    bucket_list = db.relationship('BucketList', backref="bucket", lazy='dynamic')

    def __repr__(self):
        return '<User %s>' % self.username


class BucketList(db.Model):
    """Model for Bucket."""
    __tablename__= 'bucketlist'

    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(64), unique=True)
    items = db.relationship('Item', backref="items", lazy='dynamic')
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    date_modified = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))

    def __repr__(self):
        return '<BucketList %s>' % self.name



class Item(db.Model):
    """Modelfor BucketList."""
    __tablename__ = 'item'

    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(64), unique=True)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    date_modified = db.Column(db.DateTime, default=datetime.utcnow)
    done = db.Column(db.Boolean, default=False)
    bucket_id = db.Column(db.Integer, db.ForeignKey("bucketlist.id"))

    def __repr__(self):
        return '<Item %s>' % self.name
