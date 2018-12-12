import random
import unittest
from app import create_app
from app.api.v1.users.models import user_list, ListModel    


class UserTest(unittest.TestCase):

    def setUp(self):

        app = create_app('testing')
        self.client = app.test_client()

    def tearDown(self):
        user_list.clear()

    def test_it_registers_user(self):

        response = self.client.post('api/v1/auth/signup', json={
            'username': 'jasuba',
            'firstname': 'Vincent',
            'lastname': 'Odhiambo',
            'email': 'user@admin.com',
            'password': 'pAsSw0rd',
        })
        print(response.get_json())
        self.assertEqual(201, response.status_code)
        self.assertEqual('jasuba', response.get_json()['username'])
        self.assertNotIn('password', response.get_json())

    def test_it_fetches_list_of_users(self):

        # setup
        user_list.append({
            'id': 2,
            'username': 'jasuba',
            'firstname': 'Vincent',
            'lastname': 'Odhiambo',
            'email': 'user@admin.com',
            'password': 'pAsSw0rd',
        })

        user_list.append({
            'id': 1,
            'username': 'another',
            'firstname': 'Gender',
            'lastname': 'Balance',
            'email': 'gb@user.com',
            'password': 'pAsSw0rd',
        })

        # act
        response = self.client.get('api/v1/users')

        # assert
        self.assertEqual(200, response.status_code)
        self.assertEqual(2, len(response.get_json()['data']))
        self.assertNotIn('password', random.choice(response.get_json()['data']))

    def test_it_fetches_users_by_id(self):
        # setup
        user_list.append({
            'id': 1,
            'username': 'jasuba',
            'firstname': 'Vincent',
            'lastname': 'Odhiambo',
            'email': 'user@admin.com',
            'password': 'pAsSw0rd',
        })

        user_list.append({
            'id': 2,
            'username': 'another',
            'firstname': 'Gender',
            'lastname': 'Balance',
            'email': 'gb@user.com',
            'password': 'pAsSw0rd',
        })

        target_id = random.choice([1, 2])
        # act
        response = self.client.get('api/v1/users/{}'.format(target_id))

        # assert
        self.assertEqual(200, response.status_code)
        self.assertEqual(target_id, response.get_json()['id'])
        self.assertNotIn('password', response.get_json())

    def test_it_updates_user_record(self):

        user_list.append({
            'id': 1,
            'username': 'jasuba',
            'firstname': 'Vincent',
            'lastname': 'Odhiambo',
            'email': 'user@admin.com',
            'password': 'pAsSw0rd',
        })

        user_list.append({
            'id': 2,
            'username': 'another',
            'firstname': 'Gender',
            'lastname': 'Balance',
            'email': 'gb@user.com',
            'password': 'pAsSw0rd',
        })

        target_id = random.choice([1, 2])
        # act
        response = self.client.patch('api/v1/users/{}'.format(target_id), json={
            'email': 'anotheremail@gmail.com'
        })

        # assert
        self.assertEqual(200, response.status_code)
        self.assertEqual('anotheremail@gmail.com',
                         response.get_json()['email'])
        self.assertIsNotNone(ListModel(user_list).find(target_id))
        self.assertEqual(ListModel(user_list).find(target_id), response.get_json())

    def test_it_validates_email_format(self):

        # act
        # make request without lastname
        response = self.client.post('api/v1/auth/signup', json={
            'username': 'jasuba',
            'firstname': 'Vincent',
            'lastname': 'Kapipi',
            'email': 'invalid email',
            'password': 'pAsSw0rd',
        })

        # assert
        self.assertEqual(422, response.status_code)
        self.assertEqual('Invalid data received',
                         response.get_json()['message'])

    def test_registration_with_duplicate_email_fails(self):
        # setup
        user_list.append({
            'id': 1,
            'username': 'jasuba',
            'firstname': 'Vincent',
            'lastname': 'Odhiambo',
            'email': 'user@admin.com',
            'password': 'pAsSw0rd',
        })

        # act
        response = self.client.post('api/v1/auth/signup', json={
            'username': 'another_user_name',
            'firstname': 'James',
            'lastname': 'Karuga',
            'email': 'user@admin.com',
            'password': 'pAsSw0rd',
        })

        # assert
        self.assertEqual(422, response.status_code)
        self.assertEqual('email already in use',
                         response.get_json()['message'])

    def test_registration_with_duplicate_username_fails(self):
        # setup
        user_list.append({
            'id': 1,
            'username': 'jasuba',
            'firstname': 'Vincent',
            'lastname': 'Odhiambo',
            'email': 'user@admin.com',
            'password': 'pAsSw0rd',
        })

        # act
        response = self.client.post('api/v1/auth/signup', json={
            'username': 'jasuba',
            'firstname': 'James',
            'lastname': 'Karuga',
            'email': 'valid@admin.com',
            'password': 'pAsSw0rd',
        })

        # assert
        self.assertEqual(422, response.status_code)
        self.assertEqual('username already taken',
                         response.get_json()['message'])

    def test_it_validates_required_fields(self):
        response = self.client.post('api/v1/auth/signup', json={})

        self.assertEqual(422, response.status_code)
        self.assertEqual('Invalid data received',
                         response.get_json()['message'])
        self.assertEqual({
            'email': ['Missing data for required field.'],
            'firstname': ['Missing data for required field.'],
            'lastname': ['Missing data for required field.'],
            'password': ['Missing data for required field.'],
            'username': ['Missing data for required field.']
        }, response.get_json()['errors'])


if __name__ == "__main__":
    unittest.main()
