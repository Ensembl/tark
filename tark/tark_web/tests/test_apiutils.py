from django.test import RequestFactory, TestCase
from tark_web.utils.apiutils import ApiUtils


class ApiUtilsTest(TestCase):
    def setUp(self):
        # Every test needs access to the request factory.
        self.factory = RequestFactory()

    def test_details(self):
        # Create an instance of a GET request.
        request = self.factory.get('/api')
        host_url = ApiUtils.get_host_url(request)
        print("Host url " + host_url)
        self.assertEqual("http://testserver", host_url, "Got the testserver url")
