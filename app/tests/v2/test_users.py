import unittest
from flask import g
from app import create_app
from app.api.v2.roles.roles import Role
from app.api.v2.users.models import UserModel
from manage import migrate, truncate, seed


class UserTest(unittest.TestCase):

    def setUp(self):
        app = create_app('testing')
        self.app_context = app.app_context()
        self.app_context.push()
        self.client = app.test_client()
        self.db = UserModel()
        migrate(g.conn)
        seed(g.conn)

        self.user_role = {
            'role_name': 'User',
            'role_slug': 'user'
        }

        self.admin_role = {
            'role_name': 'Administrator',
            'role_slug': 'admin'
        }

        self.sample_user = {
            'username': 'vino',
            'firstname': 'Vincent',
            'lastname': 'Odhiambo',
            'email': 'user@admin.com',
            'password': 'PaSsw0rd',
        }

        self.auth = self.client.post('api/v2/auth/login', json={
            'username': self.sample_user['username'],
            'password': self.sample_user['password']
        })

        self.access_token = self.auth.get_json()['access_token']

        self.headers = {
            'Authorization': 'Bearer {}'.format(self.access_token)
        }

    def tearDown(self):
        truncate(g.conn)

    def test_it_registers_user(self):
        # setup
        Role().save(self.user_role)
        self.sample_user.update({
            'username': 'another_username',
            'email': 'another@email.com'
        })
        # act
        response = self.client.post('api/v2/auth/signup', json=self.sample_user, headers=self.headers)

        self.assertEqual(201, response.status_code)
        self.assertEqual(self.sample_user['username'], response.get_json()['username'])
        self.assertNotIn('password', response.get_json())

    def test_it_fetches_list_of_users(self):
        # setup
        Role().save(self.user_role)
        self.db.save(self.sample_user)

        self.sample_user.update({
            'username': 'second_user',
            'email': 'newemail@email.com'
        })

        self.db.save(self.sample_user)

        # act
        response = self.client.get('api/v2/users', headers=self.headers)

        # assert
        self.assertEqual(200, response.status_code)
        self.assertEqual(3, len(response.get_json()['data']))

    def test_it_fetches_users_by_id(self):
        # setup
        Role().save(self.user_role)
        self.db.save(self.sample_user)

        # act
        response = self.client.get('api/v2/users/1', headers=self.headers)
        failing = self.client.get('api/v2/users/5', headers=self.headers)

        # assert
        self.assertEqual(200, response.status_code)
        self.assertEqual(self.sample_user['username'], response.get_json()['username'])
        self.assertEqual(404, failing.status_code)
        self.assertEqual('resource not found', failing.get_json()['message'])

    def test_it_updates_user_record(self):
        # setup
        Role().save(self.user_role)
        self.db.save(self.sample_user)

        # act
        username = 'a_new_username'
        response = self.client.patch('api/v2/users/1', json={
            'username': username
        }, headers=self.headers)

        # assert
        self.assertEqual(200, response.status_code)
        self.assertEqual(username, response.get_json()['username'])

    def test_it_validates_email_format(self):
        # setup
        # act
        self.sample_user.update({
            'email': 'not valid email'
        })
        response = self.client.post('api/v2/auth/signup', json=self.sample_user, headers=self.headers)

        # assert
        self.assertEqual(422, response.status_code)
        self.assertEqual(['Not a valid email address.', 'The parameter must be a valid email'],
                         response.get_json()['errors']['email'])

    def test_registration_with_duplicate_email_fails(self):
        # setup
        Role().save(self.user_role)
        self.db.save(self.sample_user)

        # act
        self.sample_user.update({
            'username': 'something_new',
            'password': 'Kab3!Eds'
        })

        response = self.client.post('api/v2/auth/signup', json=self.sample_user)

        # assert
        self.assertEqual(422, response.status_code)
        self.assertEqual('error, email already in use', response.get_json()['message'])

    def test_registration_with_duplicate_username_fails(self):
        # setup
        Role().save(self.user_role)
        self.db.save(self.sample_user)

        # act
        self.sample_user.update({
            'password': 'Kab3!Eds',
            'email': 'new@anewemail.com'
        })

        response = self.client.post('api/v2/auth/signup', json=self.sample_user)

        # assert
        self.assertEqual(422, response.status_code)
        self.assertEqual('error, username already taken', response.get_json()['message'])

    def test_it_validates_required_fields(self):
        # setup
        Role().save(self.user_role)

        # act
        response = self.client.post('api/v2/auth/signup', json={})

        # assert
        self.assertEqual(422, response.status_code)
        self.assertEqual(5, len(response.get_json()['errors']))


if __name__ == "__main__":
    unittest.main()
