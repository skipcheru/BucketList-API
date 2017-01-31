import unittest
from flask import json
from app import db, create_app
from app.models import User


class TestBase(unittest.TestCase):
    """TestBase class for all test classes."""

    def setUp(self):
        self.app = create_app('testing')
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        # register user and use the toke for authorization
        data = json.dumps({'username': 'kiki', 'password': 'shesheni'})
        url, mime_type = '/api/v1/auth/register', 'application/json'
        response = self.client.post(url, data=data, content_type=mime_type)

        # Login and get access_token
        data = json.dumps({'username': 'kiki', 'password': 'shesheni'})
        url, mime_type = '/api/v1/auth/login', 'application/json'
        response = self.client.post(url, data=data, content_type=mime_type)
        token = json.loads(response.data)
        self.headers = {'Authorization': 'JWT ' + token['access_token']}

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()
