import json
import unittest

from app import create_app, db

from tests.utils import create_product_area


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
        """Test API can create a product_area"""
        res = create_product_area(self)
        self.assertIn('Area1', str(res.data))
        # it must not be possible to create without a name
        res = self.client_instance().post('/api/product-areas/', data=json.dumps({}))
        self.assertEqual(res.status_code, 400)

    def test_api_can_get_all_product_areas(self):
        """Test API can get a product area."""
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

if __name__ == "__main__":
    unittest.main()
