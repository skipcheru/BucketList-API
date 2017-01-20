import unittest
from app import db, create_app
from app.models import User
import json


class ApiTestCase(unittest.TestCase):
    """Tests for API"""

    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        self.client = self.app.test_client()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    # test register
    def test_register(self):
        data = json.dumps({'username': 'kiki', 'password': 'nuf'})
        url, mime_type = 'auth/register', 'application/json'
        response = self.client.post(url, data=data, content_type=mime_type)
        json_response = json.loads(response.data.decode('utf-8'))
        self.assertEqual(response.status_code, 201)
        self.assertEqual('User registered sucessfully',
                         json_response['message'])

    # test register existing user
    def test_register_existing_user(self):
        user = User(username='kim', password='kim')
        db.session.add(user)
        db.session.commit()
        # register same user
        data = json.dumps({'username': 'kim', 'password': 'kim'})
        url, mime_type = 'auth/register', 'application/json'
        response = self.client.post(url, data=data, content_type=mime_type)
        json_response = json.loads(response.data.decode('utf-8'))
        self.assertEqual(response.status_code, 409)
        self.assertEqual('User already exists', json_response['message'])

    # test invalid content_type
    def test_invalid_mime_type(self):
        data = json.dumps({'username': 'kiki', 'password': 'nuf'})
        url, mime_type = 'auth/register', 'application/text/html'
        response = self.client.post(url, data=data, content_type=mime_type)
        self.assertEqual(response.status_code, 415)

    # Test login
    def test_login(self):
        data = json.dumps({'username': 'kiki', 'password': 'nuf'})
        url, mime_type = 'auth/login', 'application/json'
        response = self.client.post(url, data=data, content_type=mime_type)
        self.assertEqual(response.status_code, 200)
