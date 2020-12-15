import falcon
from falcon import testing
from service.start import app

class ResourcesTestCase(testing.TestCase):
    def setUp(self):
        super(ResourcesTestCase, self).setUp()

        self.app = app