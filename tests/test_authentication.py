from flask import json
from base_class import TestBase


class ApiTestCase(TestBase):
    """Tests for Authentication"""

    # test register
    def test_register(self):
        # test register with valid credentials
        data = json.dumps({'username': 'shem', 'password': 'shem123'})
        url, mime_type = 'api/v1/auth/register', 'application/json'
        response = self.client.post(url, data=data, content_type=mime_type)
        self.assertEqual(response.status_code, 201)

        response = json.loads(response.data)
        self.assertEqual('User registered successfully', response['message'])

        # test register existing user
        data = json.dumps({'username': 'kiki', 'password': 'nuf'})
        url, mime_type = 'api/v1/auth/register', 'application/json'
        response = self.client.post(url, data=data, content_type=mime_type)
        self.assertEqual(response.status_code, 409)

        response = json.loads(response.data)
        self.assertEqual('User already exists', response['error'])

        # test registration with missing password
        data = json.dumps({'username': 'doodle', 'password': ''})
        url, mime_type = 'api/v1/auth/register', 'application/json'
        response = self.client.post(url, data=data, content_type=mime_type)
        self.assertEqual(response.status_code, 400)

        response = json.loads(response.data)
        self.assertEqual(response['error'], 'username and password required')

        # test registration with missing username
        data = json.dumps({'username': '', 'password': 'ninjax'})
        url, mime_type = 'api/v1/auth/register', 'application/json'
        response = self.client.post(url, data=data, content_type=mime_type)
        self.assertEqual(response.status_code, 400)

        response = json.loads(response.data)
        self.assertEqual(response['error'], 'username and password required')

        # test invalid content_type
        data = json.dumps({'username': 'kiki', 'password': 'nuf'})
        url, mime_type = 'api/v1/auth/register', 'application/text/html'
        response = self.client.post(url, data=data, content_type=mime_type)
        self.assertEqual(response.status_code, 415)

        # Test login
    def test_login(self):
        data = json.dumps({'username': 'kiki', 'password': 'shesheni'})
        url, mime_type = 'api/v1/auth/login', 'application/json'
        response = self.client.post(url, data=data, content_type=mime_type)
        self.assertEqual(response.status_code, 200)

        response = json.loads(response.data)
        self.assertIn('access_token', response)

        # test user is not authenticated with invalid credentials
        data = json.dumps({'username': '123', 'password': '123'})
        url, mime_type = 'api/v1/auth/login', 'application/json'
        response = self.client.post(url, data=data, content_type=mime_type)
        self.assertEqual(response.status_code, 401)

        # test user is not authenticated with password or username missing
        data = json.dumps({'username': '', 'password': ''})
        url, mime_type = 'api/v1/auth/login', 'application/json'
        response = self.client.post(url, data=data, content_type=mime_type)
        self.assertEqual(response.status_code, 400)
