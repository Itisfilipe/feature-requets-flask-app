import json
import unittest

from app import create_app, db

from tests.utils import create_client, create_feature, create_product_area


class FeatureTestCase(unittest.TestCase):
    """This class represents the feature test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app(config_name="testing")
        self.client_instance = self.app.test_client
        self.product_area = json.dumps({'name': 'Area1'})
        self.client = json.dumps({'name': 'Client1'})
        self.feature_no_title = json.dumps({
            'clientId': 1,
            'date': "2017-06-07",
            'description': "some description",
            'priority': 1,
            'productAreaId': 1
        })
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
        """Test API can create a feature"""
        # It must not be possible to create a feature without client and
        # product area
        res = self.client_instance().post('/api/features/', data=self.feature)
        self.assertEqual(res.status_code, 404)
        # it must not be possible to create without a parameter
        res = self.client_instance().post('/api/features/', data=self.feature_no_title)
        self.assertEqual(res.status_code, 400)
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
        """Test API can get all features."""
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
        """Test API can edit an existing feature. (not priority)"""
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
        """Test API can delete an existing feature."""
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
        """Test if priorities for some client will reorganize after edit the priority info"""
        create_product_area(self)
        create_client(self)
        create_client(self)
        create_feature(self)
        create_feature(self, self.feature2)
        create_feature(self, self.feature2)
        create_feature(self, self.feature3)
        create_feature(self, self.feature3)
        # get data with priority 4
        res = self.client_instance().get('/api/features/2')
        data_obj = json.loads(res.get_data(as_text=True))
        # edit priority from 4 to 2
        data_obj["priority"] = 2
        # fixing client and product area info
        data_obj["clientId"] = data_obj["client"]["id"]
        data_obj["productAreaId"] = data_obj["productArea"]["id"]
        # deleting irrelevant data
        del data_obj["client"]
        del data_obj["productArea"]
        self.client_instance().patch('/api/features/2', data=json.dumps(data_obj))
        res = self.client_instance().get('/api/features')
        data_obj = json.loads(res.get_data(as_text=True))
        # organize features by priority and them check if they are right
        features = sorted(data_obj, key=lambda i: i["priority"])
        for index, feature in enumerate(features, 1):
            if feature["id"] == 2:
                # priority was changed properly
                self.assertEqual(2, feature["priority"])
                continue
            # check if priorities are in order
            self.assertEqual(index, feature["priority"])

    def test_priority_reorganization_when_editing_with_different_client(self):
        """Test if priorities for some client will reorganize after edit the client"""
        create_product_area(self)
        create_client(self)
        create_client(self)
        create_feature(self)
        create_feature(self, self.feature2)
        create_feature(self, self.feature2)
        create_feature(self, self.feature3)
        # get data with priority 4
        res = self.client_instance().get('/api/features/2')
        data_obj = json.loads(res.get_data(as_text=True))
        # change client id
        data_obj["clientId"] = 2
        data_obj["productAreaId"] = data_obj["productArea"]["id"]
        del data_obj["client"]
        del data_obj["productArea"]
        self.client_instance().patch('/api/features/2', data=json.dumps(data_obj))
        res = self.client_instance().get('/api/features/2')
        feature = json.loads(res.get_data(as_text=True))
        # priority must be 1 because theres only one feature for that client
        self.assertEqual(1, feature["priority"])

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
        # check all priorities will be right
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
