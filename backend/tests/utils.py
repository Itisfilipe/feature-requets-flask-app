def create_client(self):
    """ Helper for create a client """
    res = self.client_instance().post('/api/clients/', data=self.client)
    self.assertEqual(res.status_code, 201)
    return res


def create_product_area(self):
    """ Helper for create a product area """
    res = self.client_instance().post('/api/product-areas/', data=self.product_area)
    self.assertEqual(res.status_code, 201)
    return res


def create_feature(self, feature=None):
    """ Helper for create a feature """
    if (feature is None):
        res = self.client_instance().post('/api/features/', data=self.feature)
    else:
        res = self.client_instance().post('/api/features/', data=feature)
    self.assertEqual(res.status_code, 201)
    return res