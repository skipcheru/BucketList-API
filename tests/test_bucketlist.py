from flask import json
from base_class import TestBase


class TestBucketList(TestBase):
    """TestBucketList class that has all test for bucketlist."""

    def test_authorization(self):
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
        data, mime_type = {'name': 'BucketList A'}, 'application/json'
        url = 'api/v1/bucketlists/'
        response = self.client.post(
            url, data=data, headers=self.headers, content_type=mime_type)
        self.assertEqual(response.status_code, 201)

    def test_get_bucketlist(self):
        # Get all bucketlists
        buckets = json.dumps([{'id': 1,
                               'name': 'BucketList A',
                               'items': [],
                               'date_created': '2016-01-23 18:58:00',
                               'date_modified': '',
                               'created_by': 'kiki'
                               }])

        mime_type, url = 'application/json', 'api/v1/bucketlists'
        response = self.client.get(
            url, headers=self.headers, content_type=mime_type)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, buckets)

        # test get single bucketlist
        mime_type, url = 'application/json', 'api/v1/bucketlists/1'
        response = self.client.get(
            url, headers=self.headers, content_type=mime_type)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, buckets)

    def test_update_bucketlist(self):
        # test update existing bucketlist
        data = json.dumps({'name': 'BucketList A'})
        url, mime_type = 'api/v1/bucketlists/1', 'application/json'
        response = self.client.put(
            url, data=data, headers=self.headers, content_type=mime_type)
        self.assertEqual(response.status_code, 200)

        response = json.loads(response.data)
        self.assertEqual(response['message'],
                         'BucketList updated successfully')

        # test update non-existing bucketlist
        url = 'api/v1/bucketlists/0'
        response = self.client.put(
            url, data=data, headers=self.headers, content_type=mime_type)
        self.assertEqual(response.status_code, 404)

        response = json.loads(response.data)
        self.assertEqual(response.data['message'], 'BucketList not found')

    def test_delete_bucketlist(self):
        # test update existing bucketlist
        url = 'api/v1/bucketlists/1'
        response = self.client.delete(
            url, headers=self.headers, content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['message'],
                         'BucketList deleted successfully')

        # test update non-existing bucketlist
        response = self.client.delete(
            'api/v1/bucketlists/0', content_type='application/json')
        self.assertEqual(response.status_code, 404)
        response = json.loads(response.data)
        self.assertEqual(response['message'], 'BucketList not found')


class TestBucketListItem(TestBase):
    """docstring for TestBucketListItem."""

    def test_get_bucketlist_item(self):
        # Get all bucketlists
        item = json.dumps({'id': 1,
                           'name': 'Notify client on the bug fix',
                           'date_created': '2016-01-23 18:58:00',
                           'date_modified': '',
                           'done': False
                           })

        mime_type, url = 'application/json', 'api/v1/bucketlists/1/items/1'
        response = self.client.get(
            url, headers=self.headers, content_type=mime_type)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, item)

    def test_update_bucketlist_item(self):
        # test update existing bucketlist
        data, url = {'name': 'Update Api'}, 'api/v1/bucketlists/1/items/1'
        response = self.client.put(
            url, headers=self.headers, content_type='application/json')
        self.assertEqual(response.status_code, 200)
        response = json.loads(response.data)
        self.assertEqual(response['message'],
                         'BucketList updated successfully')

        # test update non-existing bucketlist
        url = 'api/v1/bucketlists/0'
        response = self.client.put(
            url, headers=self.headers, content_type='application/json')
        self.assertEqual(response.status_code, 404)
        response = json.loads(response.data)
        self.assertEqual(response['message'], 'BucketList not found')

        # test update existing bucketlist done to True
        data, url = {'done': True}, 'api/v1/bucketlists/1/items/1'
        response = self.client.put(
            url, data=data, headers=self.headers, content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['message'],
                         'BucketList updated successfully')

    def test_delete_bucketlist_item(self):
        # test delete existing bucketlist
        url, mime_type = 'api/v1/bucketlists/1/items/1', 'application/json'
        response = self.client.delete(
            url, headers=self.headers, content_type=mime_type)
        self.assertEqual(response.status_code, 200)
        response = json.loads(response.data)
        self.assertEqual(response['message'],
                         'BucketList deleted successfully')

        # test delete non-existing bucketlist
        url = 'api/v1/bucketlists/1/items/0'
        response = self.client.delete(
            url, headers=self.headers, content_type=mime_type)
        self.assertEqual(response.status_code, 404)
        response = json.loads(response.data)
        self.assertEqual(response['message'], 'BucketList not found')
