import unittest
from app.models import AccessRequest


class AccessModelTest(unittest.TestCase):

    def create_access_request(self):
        self.access = AccessRequest.objects.create(
            space_name="главный офис",
            name="Иванов Иван Иванович",
            type="manager",
            access="yes",
            date="2018-10-1",
        )
        return self.access

    def test_access_request_creation(self):
        new_access = self.create_access_request()
        self.assertTrue(isinstance(new_access, AccessRequest))


