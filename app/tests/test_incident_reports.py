import unittest
import json
from app import create_app
from app.api.v1.incidents.models import incident_list


class TestInterventionRecords(unittest.TestCase):

    def setUp(self):
        self.app = create_app()
        self.app.testing = True
        self.client = self.app.test_client()
        self.test_record = {
            "title": "NTSA Officer asking for bribe",
            "description": "lorem ipsum dolor sit amet",
            "location": {
                "lat": -1.23121,
                "lng": 23.45443
            },
            "type": "intervention record"
        }

    def tearDown(self):
        incident_list.clear()

    def test_it_creates_incident_records(self):

        response = self.client.post('api/v1/incidents', json={
            "title": "Damaged roads in Matuu",
            "description": "lorem ipsum dolor sit amet",
            "location": {
                "lat": -1.23121,
                "lng": 23.45443
            },
            "type": "intervention record"
        })

        second_response = self.client.post('api/v1/incidents', json={
            "title": "NTSA Officer asking for bribe",
            "description": "lorem ipsum dolor sit amet",
            "location": {
                "lat": -1.23121,
                "lng": 23.45443
            },
            "type": "red flag"
        })

        self.assertEqual(201, response.status_code)
        self.assertEqual(201, second_response.status_code)
        self.assertEqual(response.get_json(), {
            'message': 'Successfully created incident report'})

    def test_it_fetches_incident_record_list(self):

        # setup
        # create items
        self.client.post('api/v1/incidents', json={
            "title": "Damaged roads in Matuu",
            "description": "lorem ipsum dolor sit amet",
            "location": {
                "lat": -1.23121,
                "lng": 23.45443
            },
            "type": "intervention record"
        })

        self.client.post('api/v1/incidents', json={
            "title": "NTSA Officer asking for bribe",
            "description": "lorem ipsum dolor sit amet",
            "location": {
                "lat": -1.23121,
                "lng": 23.45443
            },
            "type": "red flag"
        })

        # act
        # fetch list
        response = self.client.get('api/v1/incidents')

        # assert
        self.assertEqual(200, response.status_code)
        self.assertEqual(2, len(response.get_json()['data']))

    def test_it_fetches_incident_with_id(self):

        # setup
        # create items
        self.client.post('api/v1/incidents', json={
            "title": "Damaged roads in Matuu",
            "description": "lorem ipsum dolor sit amet",
            "location": {
                "lat": -1.23121,
                "lng": 23.45443
            },
            "type": "intervention record"
        })

        self.client.post('api/v1/incidents', json={
            "title": "NTSA Officer asking for bribe",
            "description": "lorem ipsum dolor sit amet",
            "location": {
                "lat": -1.23121,
                "lng": 23.45443
            },
            "type": "red flag"
        })

        response = self.client.get('api/v1/incidents/1')
        failed_response = self.client.get('api/v1/incidents/3434')

        self.assertEqual(200, response.status_code)
        self.assertTrue(set(self.test_record).issubset(
            set(response.get_json())))
        self.assertEqual(404, failed_response.status_code)
        self.assertEqual(failed_response.get_json(), {
                         'message': 'resource not found', 'status': 404})

    def test_it_fetches_incidents_by_type(self):

        # setup
        # create items
        self.client.post('api/v1/incidents', json={
            "title": "Damaged roads in Matuu",
            "description": "lorem ipsum dolor sit amet",
            "location": {
                "lat": -1.23121,
                "lng": 23.45443
            },
            "type": "intervention record"
        })

        self.client.post('api/v1/incidents', json={
            "title": "NTSA Officer asking for bribe",
            "description": "lorem ipsum dolor sit amet",
            "location": {
                "lat": -1.23121,
                "lng": 23.45443
            },
            "type": "red flag"
        })

        response = self.client.get('api/v1/incidents/red flag')
        wrong_type = self.client.get('api/v1/incidents/nonexistent type')

        self.assertEqual(200, response.status_code)
        self.assertEqual(200, wrong_type.status_code)
        self.assertEqual(0, len(wrong_type.get_json()['data']))
        self.assertEqual(1, len(response.get_json()['data']))

    def test_it_updates_incident_records(self):

        # setup
        # create items
        self.client.post('api/v1/incidents', json={
            "title": "Damaged roads in Matuu",
            "description": "lorem ipsum dolor sit amet",
            "location": {
                "lat": -1.23121,
                "lng": 23.45443
            },
            "type": "intervention record"
        })

        response = self.client.patch('api/v1/incidents/1', json={
            'description': 'changed description message',
            'location': {
                'lat': 1.22222,
                'lng': 12.11111
            }
        })

        self.assertEqual(200, response.status_code)
        self.assertEqual('changed description message',
                         response.get_json()['description'])

    def test_updating_nonexistent_record_fails(self):
        response = self.client.patch('api/v1/incidents/1', json={
            'description': 'changed description message',
            'location': {
                'lat': 1.22222,
                'lng': 12.11111
            }
        })

        self.assertEqual(404, response.status_code)
        self.assertEqual({'message': 'resource not found', 'status': 404}, response.get_json())

    def test_it_deletes_incident_records_by_id(self):
        # setup
        # create items
        self.client.post('api/v1/incidents', json={
            "title": "Damaged roads in Matuu",
            "description": "lorem ipsum dolor sit amet",
            "location": {
                "lat": -1.23121,
                "lng": 23.45443
            },
            "type": "intervention record"
        })

        incident_id = 1

        response = self.client.delete(
            'api/v1/incidents/{}'.format(incident_id))

        self.assertEqual(200, response.status_code)
        self.assertEqual(incident_id, response.get_json()['data'][0]['id'])


if __name__ == "__main__":
    unittest.main()
