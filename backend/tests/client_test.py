import json
import unittest

from app import create_app, db

from tests.utils import create_client, create_feature, create_product_area


class ClientTestCase(unittest.TestCase):
    """This class represents the client test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app(config_name="testing")
        self.client_instance = self.app.test_client
        self.client = json.dumps({'name': 'Client1'})
        self.product_area = json.dumps({'name': 'Area1'})
        self.feature = json.dumps({
            'clientId': 1,
            'date': "2017-06-07",
            'description': "some description",
            'priority': 1,
            'productAreaId': 1,
            'title': "some title"
        })
        with self.app.app_context():
            db.create_all()

    def test_client_creation(self):
        """Test API can create a client (POST request)"""
        res = create_client(self)
        self.assertIn('Client1', str(res.data))
        # it must not be possible to create without a name
        res = self.client_instance().post('/api/clients/', data=json.dumps({}))
        self.assertEqual(res.status_code, 400)

    def test_api_can_get_all_clients(self):
        """Test API can get a client (GET request)."""
        create_client(self)
        res = self.client_instance().get('/api/clients/')
        data = res.get_data(as_text=True)
        self.assertEqual(res.status_code, 200)
        # Client1 must be inside of the returned data
        self.assertIn('Client1', data)
        # We expect the data to be a list of clients
        self.assertEqual(type(json.loads(data)), list)

    def test_client_max_priorities_equal_to_n_features_plus_one(self):
        """Test if client has the number of max priorities equal the number of features plus one."""
        create_product_area(self)
        create_client(self)
        create_feature(self)
        res = self.client_instance().get('/api/clients/')
        self.assertEqual(res.status_code, 200)
        data = json.loads(res.get_data(as_text=True))
        max_priority = data[0]["maxPriorities"]
        # priority max must be equal to n of features + 1
        self.assertEqual(max_priority, 2)
        create_feature(self)
        res = self.client_instance().get('/api/clients/')
        self.assertEqual(res.status_code, 200)
        data = json.loads(res.get_data(as_text=True))
        max_priority = data[0]["maxPriorities"]
        # priority max must be equal to n of features + 1
        self.assertEqual(max_priority, 3)

    def tearDown(self):
        """teardown all initialized variables."""
        with self.app.app_context():
            db.session.remove()
            db.drop_all()


if __name__ == "__main__":
    unittest.main()
