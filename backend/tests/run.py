from coverage import coverage
import unittest


cov = coverage(branch=True, include=['app/*'])
cov.set_option('report:show_missing', True)
cov.erase()
cov.start()

from .client_test import ClientTestCase
from .features_test import FeatureTestCase
from .product_area_test import ProductAreaTestCase

if __name__ == '__main__':
    tests = unittest.TestLoader().discover('./tests', pattern='*test.py')
    unittest.TextTestRunner(verbosity=1).run(tests)
    cov.stop()
    cov.save()
    print("\n\nCoverage Report:\n")
    cov.report()