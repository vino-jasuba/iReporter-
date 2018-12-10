import random
import unittest
from flask import g
from app import create_app
from app.api.v2.incidents.models import IncidentModel
from app.api.v2.users.models import UserModel
from app.api.v2.roles.roles import Role
from manage import migrate, truncate, seed


class TestIncidentReports(unittest.TestCase):

    def setUp(self):
        app = create_app('testing')
        self.app_context = app.app_context()
        self.app_context.push()
        self.client = app.test_client()
        self.db = IncidentModel()
        migrate(g.conn)
        seed(g.conn)

        self.red_flag = {
            "title": "NTSA Officer asking for bribe",
            "description": "lorem ipsum dolor sit amet",
            "location": {
                "lat": -1.23121,
                "lng": 23.45443
            },
            "incident_type": "red flag",
            "created_by": 1,
            "status": "pending"
        }

        self.intervention_record = {
            "title": "Damaged roads in Matuu",
            "description": "lorem ipsum dolor sit amet",
            "location": {
                "lat": -1.23121,
                "lng": 23.45443
            },
            "incident_type": "intervention record",
            "created_by": 1,
            "status": "pending"
        }

        self.user_role = {
            'role_name': 'User',
            'role_slug': 'user'
        }

        self.admin_role = {
            'role_name': 'Administrator',
            'role_slug': 'admin'
        }

        self.test_user = {
            'username': 'vino',
            'firstname': 'Vincent',
            'lastname': 'Odhiambo',
            'email': 'user@admin.com',
            'password': 'PaSsw0rd',
        }

        self.auth = self.client.post('api/v2/auth/login', json={
            'username': self.test_user['username'],
            'password': self.test_user['password']
        })

        self.access_token = self.auth.get_json()['access_token']

        self.headers = {
            'Authorization': 'Bearer {}'.format(self.access_token)
        }

    def tearDown(self):
        truncate(g.conn)

    def test_it_creates_incident_records(self):
        # setup
        # act
        response = self.client.post('api/v2/incidents', json=self.red_flag, headers=self.headers)

        self.assertEqual(201, response.status_code)
        self.assertEqual(response.get_json(), {
            'message': 'Successfully created incident report'})

    def test_it_validates_location_data_for_incident_records(self):
        pass

    def test_it_fetches_incident_record_list(self):
        # setup
        IncidentModel().save(self.intervention_record)
        IncidentModel().save(self.red_flag)
        # act

        response = self.client.get('api/v2/incidents', headers=self.headers)
        self.assertEqual(200, response.status_code)
        self.assertIsInstance(response.get_json()['data'], list)
        self.assertEqual(2, len(response.get_json()['data']))

    def test_it_fetches_incident_with_id(self):
        # setup
        IncidentModel().save(self.intervention_record)
        IncidentModel().save(self.red_flag)
        # act

        response = self.client.get('api/v2/incidents/1', headers=self.headers)

        failed_response = self.client.get('api/v1/incidents/3434')

        self.assertEqual(200, response.status_code)
        self.assertEqual(1, response.get_json()['id'])
        self.assertEqual('intervention record', response.get_json()['incident_type'])
        self.assertEqual(404, failed_response.status_code)
        self.assertEqual({'message': 'resource not found', 'status': 404}, failed_response.get_json())

    def test_it_fetches_incidents_by_type(self):
        # setup
        IncidentModel().save(self.intervention_record)
        IncidentModel().save(self.red_flag)

        # act
        response = self.client.get('api/v2/incidents/red flag', headers=self.headers)
        wrong_type = self.client.get('api/v2/incidents/nonexistent type', headers=self.headers)

        self.assertEqual(200, response.status_code)
        self.assertEqual(200, wrong_type.status_code)
        self.assertEqual(0, len(wrong_type.get_json()['data']))
        self.assertEqual(1, len(response.get_json()['data']))

    def test_it_updates_incident_records(self):
        # setup
        IncidentModel().save(self.intervention_record)
        IncidentModel().save(self.red_flag)
        # create items
        choice = random.choice([1, 2])
        description = 'changed description message'

        response = self.client.patch('api/v2/incidents/{}'.format(choice), json={
            'description': description,
            'location': {
                'lat': 1.22452,
                'lng': 23.2323
            }}, headers=self.headers)

        self.assertEqual(200, response.status_code)
        self.assertEqual(description,
                         response.get_json()['description'])

    def test_updating_nonexistent_record_fails(self):
        # setup
        # act
        response = self.client.patch('api/v2/incidents/1', json={
            'description': 'This is a failing request'
        }, headers=self.headers)

        # assert
        self.assertEqual(404, response.status_code)
        self.assertEqual('resource not found', response.get_json()['message'])

    def test_it_deletes_incident_records_by_id(self):
        # setup
        IncidentModel().save(self.intervention_record)
        IncidentModel().save(self.red_flag)
        # act

        choice = random.choice([1, 2])
        response = self.client.delete('api/v2/incidents/{}'.format(choice), headers=self.headers)

        # assert
        response_data = response.get_json()['data'][0]
        self.assertEqual(200, response.status_code)
        self.assertEqual(choice, response_data['id'])
        self.assertEqual('record has been deleted', response_data['message'])

    def test_admin_updates_incident_status(self):
        # setup
        IncidentModel().save(self.intervention_record)

        # act
        status = 'resolved'
        response = self.client.patch('api/v2/admin/incidents/1', json={
            'status': status
        }, headers=self.headers)

        # assert
        self.assertEqual(200, response.status_code)
        self.assertEqual(status, response.get_json()['status'])


if __name__ == "__main__":
    unittest.main()
