import random
import unittest
from app import create_app
from app.api.v1.users.models import user_list, Model



class UserTest(unittest.TestCase):

    def setUp(self):

        app = create_app('testing')
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

    def test_it_updates_user_record(self):
        
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
        response = self.client.patch('api/v1/users/{}'.format(target_id), json={
            'email': 'anotheremail@gmail.com'
        })

        # assert 
        self.assertEqual(200, response.status_code)
        self.assertEqual('anotheremail@gmail.com', response.get_json()['email'])
        self.assertIsNotNone(Model(user_list).find(target_id))
        self.assertEqual(Model(user_list).find(target_id), response.get_json())
        

    def test_it_validates_email_format(self):

        # act 
        # make request without lastname
        response = self.client.post('api/v1/auth/register', json={
            'username': 'jasuba',
            'firstname': 'Vincent',
            'lastname': 'Kapipi',
            'email': 'invalid email',
            'password': 'password',
            'password_confirm': 'password'
        })

        

        # assert 
        self.assertEqual(426, response.status_code)
        self.assertEqual('error, email provided is not a valid email', response.get_json()['message'])


    def test_registration_with_duplicate_email_fails(self):
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

        # act 
        response = self.client.post('api/v1/auth/register', json={
            'username': 'another_user_name',
            'firstname': 'James',
            'lastname': 'Karuga',
            'email': 'user@admin.com',
            'password': 'password',
            'password_confirm': 'password'
        })

        # assert 
        self.assertEqual(426, response.status_code)
        self.assertEqual('error, email already in use', response.get_json()['message'])

    def test_registration_with_duplicate_username_fails(self):
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

         # act 
        response = self.client.post('api/v1/auth/register', json={
            'username': 'jasuba',
            'firstname': 'James',
            'lastname': 'Karuga',
            'email': 'valid@admin.com',
            'password': 'password',
            'password_confirm': 'password'
        })

        # assert 
        self.assertEqual(426, response.status_code)
        self.assertEqual('error, username already taken', response.get_json()['message'])

    def test_it_requires_firstname_in_registration_input(self):

        # act 
        # make request without firstname
        response = self.client.post('api/v1/auth/register', json={
            'username': 'jasuba',
        })

        # assert 
        self.assertEqual(400, response.status_code)
        self.assertEqual('firstname field is required', response.get_json()['message']['firstname'])

    def test_it_requires_lastname_in_registration_input(self):

        # act 
        # make request without lastname
        response = self.client.post('api/v1/auth/register', json={
            'username': 'jasuba',
            'firstname': 'Vincent'
        })
  
        # assert 
        self.assertEqual(400, response.status_code)
        self.assertEqual('lastname field is required', response.get_json()['message']['lastname'])
   
    def test_it_requires_email_in_registration_input(self):

        # act 
        # make request without lastname
        response = self.client.post('api/v1/auth/register', json={
            'username': 'jasuba',
            'firstname': 'Vincent',
            'lastname': 'Kapipi'
        })

        # assert 
        self.assertEqual(400, response.status_code)
        self.assertEqual('email field is required', response.get_json()['message']['email'])


    def test_it_requires_password_confirmation_in_registration_input(self):

        # act 
        response = self.client.post('api/v1/auth/register', json={
            'username': 'jasuba',
            'firstname': 'Vincent',
            'lastname': 'Kapipi',
            'email': 'valid@email.com',
            'password': 'password'
        })

        # assert 
        self.assertEqual(400, response.status_code)
        self.assertEqual('password_confirm field is required', response.get_json()['message']['password_confirm'])  


if __name__ == "__main__":
    unittest.main()
