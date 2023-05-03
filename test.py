import unittest
import requests
import json

class FlaskGroupChatTest(unittest.TestCase):
    def setUp(self):
        self.url = 'http://localhost:5000/api'
        self.admin_user_token = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoiMSIsImV4cCI6MTY4MzEzMzIwNn0.2b3rKSu-r5U1HF56mqGB8fCimdNeycn1Xi45d9rdzjU'
        self.normal_user_token = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoiMSIsImV4cCI6MTY4MzEzMzIwNn0.2b3rKSu-r5U1HF56mqGB8fCimdNeycn1Xi45d9rdzjU'
        self.group_id = '1'
        self.message_id = '1'

    def test_create_normal_user(self):
        headers = {'Content-Type': 'application/json', 'X-API-Key':self.admin_user_token}
        data = json.dumps({
            'username': 'normal_user1',
            'password': 'normal_user1',
            'email': 'normal_user@example.com',
            'is_admin': False
        })
        response = requests.post(self.url + '/users', headers=headers, data=data)
        self.assertEqual(response.status_code, 201)
        self.assertIn('api_key', response.json())
        self.normal_user_token = response.json()['api_key']

    def test_create_group(self):
        headers = {'Content-Type': 'application/json', 'X-API-Key': self.normal_user_token}
        data = json.dumps({
            'name': 'test_group',
            'description': 'This is a test group.'
        })
        response = requests.post(self.url + '/groups', headers=headers, data=data)
        self.assertEqual(response.status_code, 201)
        self.group_id = response.json()['id']

    def test_send_message(self):
        headers = {'Content-Type': 'application/json', 'X-API-Key': self.normal_user_token}
        data = json.dumps({
            'text': 'This is a test message.'
        })
        response = requests.post(self.url + '/groups/{}/messages'.format(self.group_id), headers=headers, data=data)
        self.assertEqual(response.status_code, 201)
        self.message_id = response.json()['id']

    def test_like_message(self):
        headers = {'Content-Type': 'application/json', 'X-API-Key':  self.normal_user_token}
        response = requests.put(self.url + '/groups/{}/messages/{}/like'.format(self.group_id, self.message_id), headers=headers)
        self.assertEqual(response.status_code, 200)

    def test_delete_group(self):
        headers = {'Content-Type': 'application/json', 'X-API-Key':  self.normal_user_token}
        response = requests.delete(self.url + '/groups/{}'.format(self.group_id), headers=headers)
        self.assertEqual(response.status_code, 204)

if __name__ == '__main__':
    unittest.main()