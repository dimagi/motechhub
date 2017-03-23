from unittest2 import TestCase
from authproxy_client.client import AuthProxyClient
from authproxy_client.credential_schema import BasicAuth


class AuthProxyClientTest(TestCase):
    token = '53335a7db69de5122689ef1cbff672fe'

    @classmethod
    def setUpClass(cls):

        cls.authproxy_client = AuthProxyClient(
            server_url='http://localhost:8000', get_password=lambda token: '******')
        cls.authproxy_client.create_or_update_credential(
            cls.token, 'http://localhost:9000', auth=BasicAuth(
                username='admin',
                password='123',
            ))

    def test_proxy(self):
        requests = self.authproxy_client.requests(self.token)
        response = requests.get('/hello/world', auth=('admin', '123'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {
            u'headers': {
                u'accept': u'*/*',
                u'accept-encoding': u'gzip, deflate',
                u'authorization': u'Basic YWRtaW46MTIz',
                u'connection': u'close',
                u'host': u'localhost:9000',
                u'user-agent': u'python-requests/2.13.0'
            },
            u'method': u'GET',
            u'url': u'/hello/world'
        })
