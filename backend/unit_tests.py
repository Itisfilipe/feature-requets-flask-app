import json
import unittest

from server import create_app, db


def create_client(self):
    res = self.client_instance().post('/api/clients/', data=self.client)
    self.assertEqual(res.status_code, 201)
    return res


def create_product_area(self):
    res = self.client_instance().post('/api/product-areas/', data=self.product_area)
    self.assertEqual(res.status_code, 201)
    return res


def create_feature(self, feature=None):
    if (feature is None):
        res = self.client_instance().post('/api/features/', data=self.feature)
    else:
        res = self.client_instance().post('/api/features/', data=feature)
    self.assertEqual(res.status_code, 201)
    return res


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
        self.assertEqual(max_priority, 2)
        create_feature(self)
        res = self.client_instance().get('/api/clients/')
        self.assertEqual(res.status_code, 200)
        data = json.loads(res.get_data(as_text=True))
        max_priority = data[0]["maxPriorities"]
        self.assertEqual(max_priority, 3)

    def tearDown(self):
        """teardown all initialized variables."""
        with self.app.app_context():
            db.session.remove()
            db.drop_all()


class ProductAreaTestCase(unittest.TestCase):
    """This class represents the product area test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app(config_name="testing")
        self.client_instance = self.app.test_client
        self.product_area = json.dumps({'name': 'Area1'})
        with self.app.app_context():
            db.create_all()

    def test_product_area_creation(self):
        """Test API can create a product_area (POST request)"""
        res = create_product_area(self)
        self.assertIn('Area1', str(res.data))

    def test_api_can_get_all_product_areas(self):
        """Test API can get a product area (GET request)."""
        create_product_area(self)
        res = self.client_instance().get('/api/product-areas/')
        data = res.get_data(as_text=True)
        self.assertEqual(res.status_code, 200)
        # Area1 must be inside of the returned data
        self.assertIn('Area1', data)
        # We expect the data to be a list of product areas
        self.assertEqual(type(json.loads(data)), list)

    def tearDown(self):
        """teardown all initialized variables."""
        with self.app.app_context():
            db.session.remove()
            db.drop_all()


class FeatureTestCase(unittest.TestCase):
    """This class represents the feature test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app(config_name="testing")
        self.client_instance = self.app.test_client
        self.product_area = json.dumps({'name': 'Area1'})
        self.client = json.dumps({'name': 'Client1'})
        self.feature = json.dumps({
            'clientId': 1,
            'date': "2017-06-07",
            'description': "some description",
            'priority': 1,
            'productAreaId': 1,
            'title': "some title"
        })
        self.feature2 = json.dumps({
            'clientId': 1,
            'date': "2017-06-07",
            'description': "some description",
            'priority': 1,
            'productAreaId': 1,
            'title': "some title2"
        })
        self.feature3 = json.dumps({
            'clientId': 1,
            'date': "2017-06-07",
            'description': "some description",
            'priority': 2,
            'productAreaId': 1,
            'title': "some title3"
        })
        with self.app.app_context():
            db.create_all()

    def test_feature_creation(self):
        """Test API can create a feature (POST request)"""
        # It must not be possible to create a feature without client and
        # product area
        res = self.client_instance().post('/api/features/', data=self.feature)
        self.assertEqual(res.status_code, 404)
        create_product_area(self)
        create_client(self)
        res = create_feature(self)
        data = res.get_data(as_text=True)
        self.assertIn('some title', data)
        self.assertIn('some description', data)
        # an eager load of client and product area is expected
        self.assertIn('Client1', data)
        self.assertIn('Area1', data)

    def test_api_can_get_all_features(self):
        """Test API can get a feature (GET request)."""
        create_product_area(self)
        create_client(self)
        create_feature(self)
        res = self.client_instance().get('/api/features/')
        self.assertEqual(res.status_code, 200)
        data = res.get_data(as_text=True)
        self.assertIn('some description', data)
        # a list of features is expected
        self.assertEqual(type(json.loads(data)), list)

    def test_api_can_get_feature_by_id(self):
        """Test API can get a single feature by using it's id."""
        create_product_area(self)
        create_client(self)
        res = create_feature(self)
        data_obj = json.loads(res.get_data(as_text=True))
        result = self.client_instance().get('/api/features/{}'.format(data_obj['id']))
        self.assertEqual(result.status_code, 200)
        self.assertIn('some title', result.get_data(as_text=True))

    def test_feature_can_be_edited(self):
        """Test API can edit an existing feature. (PUT request)"""
        create_product_area(self)
        create_client(self)
        create_feature(self)

        new_feature = json.dumps({
            'clientId': 1,
            'date': "2017-06-07",
            'description': "another description",
            'priority': 1,
            'productAreaId': 1,
            'title': "another title"
        })

        res = self.client_instance().patch('/api/features/1', data=new_feature)
        self.assertEqual(res.status_code, 200)
        res = self.client_instance().get('/api/features/1')
        self.assertIn('another title', res.get_data(as_text=True))

    def test_feature_deletion(self):
        """Test API can delete an existing feature. (DELETE request)."""
        create_product_area(self)
        create_client(self)
        create_feature(self)
        res = self.client_instance().delete('/api/features/1')
        self.assertEqual(res.status_code, 200)
        # Test to see if it exists, should return a 404
        res = self.client_instance().get('/api/features/1')
        self.assertEqual(res.status_code, 404)

    def test_priority_reorganization_when_create(self):
        """Test if priorities for some client will reorganize after create"""
        create_product_area(self)
        create_client(self)
        # priority 1
        create_feature(self, self.feature)
        # priority 1
        create_feature(self, self.feature2)
        # priority 2
        create_feature(self, self.feature3)
        # priority for first id must be 3
        res = self.client_instance().get('/api/features/1')
        self.assertEqual(res.status_code, 200)
        data_obj = json.loads(res.get_data(as_text=True))
        self.assertEqual(data_obj["priority"], 3)
        # priority for first id must be 1
        res = self.client_instance().get('/api/features/2')
        self.assertEqual(res.status_code, 200)
        data_obj = json.loads(res.get_data(as_text=True))
        self.assertEqual(data_obj["priority"], 1)
         # priority for first id must be 2
        res = self.client_instance().get('/api/features/3')
        self.assertEqual(res.status_code, 200)
        data_obj = json.loads(res.get_data(as_text=True))
        self.assertEqual(data_obj["priority"], 2)


    def test_priority_reorganization_when_editing(self):
        """Test if priorities for some client will reorganize after edit"""
        create_product_area(self)
        create_client(self)
        create_feature(self)
        create_feature(self, self.feature2)
        create_feature(self, self.feature2)
        create_feature(self, self.feature3)
        create_feature(self, self.feature3)
        # get data with priority 4
        res = self.client_instance().get('/api/features/2')
        data_obj = json.loads(res.get_data(as_text=True))
        data_obj["priority"] = 2
        data_obj["clientId"] = data_obj["client"]["id"]
        data_obj["productAreaId"] = data_obj["productArea"]["id"]
        del data_obj["client"]
        del data_obj["productArea"]
        self.client_instance().patch('/api/features/2', data=json.dumps(data_obj))
        res = self.client_instance().get('/api/features')
        data_obj = json.loads(res.get_data(as_text=True))
        features = sorted(data_obj, key=lambda i: i["priority"])
        for index, feature in enumerate(features, 1):
            if feature["id"] == 2:
                # priority was changed properly
                self.assertEqual(2, feature["priority"])
            # check if priorities are in order
            self.assertEqual(index, feature["priority"])

    def test_priority_reorganization_when_delete(self):
        """Test if priorities for some client will reorganize after delete"""
        create_product_area(self)
        create_client(self)
        create_feature(self)
        create_feature(self)
        create_feature(self)
        res = self.client_instance().get('/api/features/2')
        data = json.loads(res.get_data(as_text=True))
        res = self.client_instance().delete('/api/features/2')
        self.assertEqual(res.status_code, 200)
        res = self.client_instance().get('/api/features')
        data_obj = json.loads(res.get_data(as_text=True))
        features = sorted(data_obj, key=lambda i: i["priority"])
        for index, feature in enumerate(features, 1):
            # the old object must no be in the features list
            self.assertNotEqual(data["id"], feature["id"])
            # check if priorities are with right values
            self.assertEqual(index, feature["priority"])

    def tearDown(self):
        """teardown all initialized variables."""
        with self.app.app_context():
            # drop all tables
            db.session.remove()
            db.drop_all()


if __name__ == "__main__":
    unittest.main()
