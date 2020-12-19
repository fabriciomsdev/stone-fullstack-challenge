import falcon
from falcon import testing
from service.start_tests import app
from tests.utils.datasource_layer import ResetDatabaseEachTestCase

class ResourcesTestCase(testing.TestCase):
    def setUp(self):
        super(ResourcesTestCase, self).setUp()
        
        self.app = app


class ResetAllApplicationEachTestCase(testing.TestCase, ResetDatabaseEachTestCase):
    def setUp(self):
        super(ResetAllApplicationEachTestCase, self).setUp()
        
        self.app = app