from flask import json
from tests.base_class import TestBase
from app.models import BucketList, Item


class TestBucketList(TestBase):
    """TestBucketList class that has all test for bucketlist."""

    def test_invalid_authorization(self):
        # add new bucketlist
        data, mime_type = {'name': 'BucketList A'}, 'application/json'
        url = 'api/v1/bucketlists/'
        response = self.client.post(
            url, data=data, content_type=mime_type)
        self.assertEqual(response.status_code, 401)

        response = json.loads(response.data)
        self.assertEqual(response['error'], 'Authorization Required')

    def test_create_bucketlist(self):
        # add new bucketlist
        data = json.dumps({'name': '2nd BucketList', "description": "Testing"})
        message = 'BucketList added successfully'
        url, mime_type = 'api/v1/bucketlists/', 'application/json'

        response = self.client.post(
            url, data=data, headers=self.headers, content_type=mime_type)
        self.assertEqual(response.status_code, 201)

        response = json.loads(response.data)
        self.assertEqual(response['message'], message)
        bucket = BucketList.query.filter_by(name='2nd BucketList').first()
        self.assertEqual(bucket.name, '2nd BucketList')

        # test create bucket list with same name
        response = self.client.post(
            url, data=data, headers=self.headers, content_type=mime_type)
        self.assertEqual(response.status_code, 409)

        response = json.loads(response.data)
        self.assertEqual(response['error'], 'BucketList already exists')

    # test search bucket list
    def test_search_bucketlist(self):
        # test search existing bucket list
        url, mime_type = 'api/v1/bucketlists/?q=BucketList', 'application/json'

        response = self.client.get(
            url, headers=self.headers, content_type=mime_type)
        self.assertEqual(response.status_code, 200)
        response = json.loads(response.data)

        self.assertEqual(len(response), 1)
        self.assertIn('1st BucketList', response[0]['Name'])

        # test search non existing bucket list
        url, mime_type = 'api/v1/bucketlists/?q=Alive', 'application/json'

        response = self.client.get(
            url, headers=self.headers, content_type=mime_type)
        self.assertEqual(response.status_code, 404)

        response = json.loads(response.data)
        self.assertEqual(response['error'], 'BucketList not found')

    def test_get_bucketlists(self):
        # Get all bucketlists
        data = json.dumps({
            'name': 'Camp sites',
            'description': 'A list of camp sites in kenya'
        })
        # add new bucket
        url, mime_type = 'api/v1/bucketlists/', 'application/json'
        self.client.post(url, data=data, headers=self.headers,
                         content_type=mime_type)

        response = self.client.get('api/v1/bucketlists/', headers=self.headers,
                                   content_type=mime_type)
        self.assertEqual(response.status_code, 200)
        response = json.loads(response.data)
        self.assertEqual(len(response), 2)
        self.assertIn('Camp sites', response[1]['Name'])

        # test get single bucketlist
        mime_type, url = 'application/json', 'api/v1/bucketlists/1'
        response = self.client.get(
            url, headers=self.headers, content_type=mime_type)
        self.assertEqual(response.status_code, 200)

    # test pagination
    def test_pagination(self):
        url, mime_type = 'api/v1/bucketlists/?limit=1&page=1', 'application/json'
        response = self.client.get(
            url, headers=self.headers, content_type=mime_type)
        self.assertEqual(response.status_code, 200)
        response = json.loads(response.data)

        self.assertEqual(len(response), 1)
        self.assertIn('1st BucketList', response[0]['Name'])

        # test invalid pagination params
        url, mime_type = 'api/v1/bucketlists/?limit=e&page=1', 'application/json'
        response = self.client.get(
            url, headers=self.headers, content_type=mime_type)
        self.assertEqual(response.status_code, 400)
        response = json.loads(response.data)
        self.assertEqual(response['error'],
                         'Page and limit should be Integers')

    def test_update_bucketlist(self):
        # test update existing bucketlist
        data = json.dumps({'name': 'The Name'})
        url, mime_type = 'api/v1/bucketlists/1', 'application/json'
        response = self.client.put(
            url, data=data, headers=self.headers, content_type=mime_type)
        self.assertEqual(response.status_code, 200)

        response = json.loads(response.data)
        print(response)
        self.assertEqual(response['message'],
                         'BucketList updated successfully')

        # test update bucketlist with invalid params
        data = json.dumps({'name': ' '})
        url, mime_type = 'api/v1/bucketlists/1', 'application/json'
        response = self.client.put(
            url, data=data, headers=self.headers, content_type=mime_type)
        self.assertEqual(response.status_code, 400)

        response = json.loads(response.data)
        self.assertEqual(response['error'], 'name missing from request')

        # test update non-existing bucketlist
        url = 'api/v1/bucketlists/0'
        response = self.client.put(
            url, data=data, headers=self.headers, content_type=mime_type)
        self.assertEqual(response.status_code, 404)

        response = json.loads(response.data)
        self.assertEqual(response['error'], 'BucketList not found')

    def test_delete_bucketlist(self):
        # test update existing bucketlist
        url, mime_type = 'api/v1/bucketlists/1', 'application/json'
        response = self.client.delete(
            url, headers=self.headers, content_type=mime_type)
        self.assertEqual(response.status_code, 200)

        response = json.loads(response.data)
        self.assertEqual(response['message'],
                         'BucketList deleted successfully')

        # test delete non-existing bucketlist
        url = 'api/v1/bucketlists/0'
        response = self.client.delete(
            url, headers=self.headers, content_type=mime_type)
        self.assertEqual(response.status_code, 404)
        response = json.loads(response.data)
        self.assertEqual(response['error'], 'BucketList not found')


class TestBucketListItem(TestBase):
    """docstring for TestBucketListItem."""

    def test_create_bucketlist_item(self):
        # add new bucketlist
        data = json.dumps({'name': 'An Item'})
        message = 'Item added successfully'
        url, mime_type = 'api/v1/bucketlists/1/items/', 'application/json'

        response = self.client.post(
            url, data=data, headers=self.headers, content_type=mime_type)
        self.assertEqual(response.status_code, 201)

        response = json.loads(response.data)
        self.assertEqual(response['message'], message)
        bucket = Item.query.filter_by(id=2).first()
        self.assertEqual(bucket.name, 'An Item')

    def test_get_bucketlist_item(self):
        # Get bucketlist item
        mime_type, url = 'application/json', 'api/v1/bucketlists/1/items/1'
        response = self.client.get(
            url, headers=self.headers, content_type=mime_type)
        self.assertEqual(response.status_code, 200)

        response = json.loads(response.data)
        self.assertIn('The Item', response['name'])

    # test search bucket list
    def test_update_bucketlist_item(self):
        # test update existing bucketlist
        data = json.dumps({'name': 'New Update'})
        url, mime_type = 'api/v1/bucketlists/1/items/1', 'application/json'
        response = self.client.put(
            url, data=data, headers=self.headers, content_type=mime_type)
        self.assertEqual(response.status_code, 200)

        response = json.loads(response.data)
        self.assertEqual(response['message'],
                         'Item updated successfully')

        # test update non-existing bucketlist
        url = 'api/v1/bucketlists/0'
        response = self.client.put(
            url, data=data, headers=self.headers, content_type=mime_type)
        self.assertEqual(response.status_code, 404)

        response = json.loads(response.data)
        self.assertEqual(response['error'], 'BucketList not found')

        # test update existing bucketlist done to True
        data, url = json.dumps(
            {'status': 'true'}), 'api/v1/bucketlists/1/items/1'
        response = self.client.put(
            url, data=data, headers=self.headers, content_type=mime_type)
        self.assertEqual(response.status_code, 200)

        response = json.loads(response.data)
        self.assertEqual(response['message'],
                         'Item updated successfully')

    def test_delete_bucketlist_item(self):
        # test delete existing bucketlist
        url, mime_type = 'api/v1/bucketlists/1/items/1', 'application/json'
        response = self.client.delete(
            url, headers=self.headers, content_type=mime_type)
        self.assertEqual(response.status_code, 200)
        response = json.loads(response.data)
        self.assertEqual(response['message'],
                         'Item deleted successfully')

        # test delete non-existing bucketlist
        url = 'api/v1/bucketlists/1/items/0'
        response = self.client.delete(
            url, headers=self.headers, content_type=mime_type)
        self.assertEqual(response.status_code, 404)
        response = json.loads(response.data)
        self.assertEqual(response['error'], 'Item not found')
