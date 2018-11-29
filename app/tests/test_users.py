import random
from unittest import TestCase
from app import create_app
from app.api.v1.users.models import user_list 



class UserTest(TestCase):

    def setUp(self):

        app = create_app()
        app.testing = True 
        self.client = app.test_client() 

    def tearDown(self):
        user_list.clear() 

    def test_it_registers_user(self):

        response = self.client.post('api/v1/auth/register', json={
            'username': 'jasuba',
            'firstname': 'Vincent',
            'lastname': 'Odhiambo',
            'email': 'user@admin.com',
            'password': 'password',
            'password_confirm': 'password'
        })

        self.assertEqual(201, response.status_code)
        self.assertEqual('jasuba', response.get_json()['username'])

    def test_it_fetches_list_of_users(self):

        # setup 
        user_list.append({
            'id': 2,
            'username': 'jasuba',
            'firstname': 'Vincent',
            'lastname': 'Odhiambo',
            'email': 'user@admin.com',
            'password': 'password',
            'password_confirm': 'password'
        })

        user_list.append({
            'id': 1,
            'username': 'another',
            'firstname': 'Gender',
            'lastname': 'Balance',
            'email': 'gb@user.com',
            'password': 'password',
            'password_confirm': 'password'
        })

        # act 
        response = self.client.get('api/v1/users')

        # assert 
        self.assertEqual(200, response.status_code)
        self.assertEqual(2, len(response.get_json()['data']))

    def test_it_fetches_users_by_id(self):
        # setup 
        user_list.append({
            'id': 1,
            'username': 'jasuba',
            'firstname': 'Vincent',
            'lastname': 'Odhiambo',
            'email': 'user@admin.com',
            'password': 'password',
            'password_confirm': 'password'
        })

        user_list.append({
            'id': 2,
            'username': 'another',
            'firstname': 'Gender',
            'lastname': 'Balance',
            'email': 'gb@user.com',
            'password': 'password',
            'password_confirm': 'password'
        })

        target_id = random.choice([1, 2])
        # act 
        response = self.client.get('api/v1/users/{}'.format(target_id))

        # assert 
        self.assertEqual(200, response.status_code)
        self.assertEqual(target_id, response.get_json()['id'])