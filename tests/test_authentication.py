import unittest
from flask import json
from app import db, create_app
from app.models import User


class ApiTestCase(unittest.TestCase):
    """Tests for Authentication"""

    def setUp(self):
        self.app = create_app('testing')
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    # test register
    def test_register(self):
        # test register with valid credentials
        url, mime_type = 'api/v1/auth/register', 'application/json'
        data = json.dumps({'username': 'kiki', 'password': 'nuff'})
        response = self.client.post(url, data=data, content_type=mime_type)
        user = User.query.filter_by(username='kiki').first()
        self.assertEqual(response.status_code, 201)
        self.assertEqual(user.username, 'kiki')

        response = json.loads(response.data)
        self.assertEqual('User registered successfully', response['message'])

        # test register existing user
        data = json.dumps({'username': 'kiki', 'password': 'nuff'})
        response = self.client.post(url, data=data, content_type=mime_type)
        self.assertEqual(response.status_code, 409)

        response = json.loads(response.data)
        self.assertEqual('User already exists', response['error'])

        # test registration with missing password
        data = json.dumps({'username': 'doodle', 'password': ''})
        response = self.client.post(url, data=data, content_type=mime_type)
        self.assertEqual(response.status_code, 400)

        response = json.loads(response.data)
        self.assertEqual(response['error'], 'password required')

        # test registration with missing username
        data = json.dumps({'username': '', 'password': 'ninjax'})
        response = self.client.post(url, data=data, content_type=mime_type)
        self.assertEqual(response.status_code, 400)

        response = json.loads(response.data)
        self.assertEqual(response['error'], 'username required')

        # test invalid content_type
        data = json.dumps({'username': 'kiki', 'password': 'nuf'})
        mime_type = 'application/text/html'
        response = self.client.post(url, data=data, content_type=mime_type)
        self.assertEqual(response.status_code, 415)

        # Test login
    def test_login(self):
        # register user first
        url, mime_type = 'api/v1/auth/register', 'application/json'
        data = json.dumps({'username': 'kiki', 'password': 'nuff'})
        self.client.post(url, data=data, content_type=mime_type)
        # test login
        data = json.dumps({'username': 'kiki', 'password': 'nuff'})
        url = 'api/v1/auth/login'
        response = self.client.post(url, data=data, content_type=mime_type)
        self.assertEqual(response.status_code, 200)

        response = json.loads(response.data)
        self.assertIn('access_token', response)

        # test user is not authenticated with invalid credentials
        data = json.dumps({'username': '123', 'password': '123'})
        response = self.client.post(url, data=data, content_type=mime_type)
        self.assertEqual(response.status_code, 401)

        # test user is not authenticated with password or username missing
        data = json.dumps({'username': '', 'password': ''})
        response = self.client.post(url, data=data, content_type=mime_type)
        self.assertEqual(response.status_code, 400)
