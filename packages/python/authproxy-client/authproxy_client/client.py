import base64
from urlparse import urlparse
import requests
from .credential_schema import Credential, NoneAuth

AUTH_PROXY_TOKEN_PASSWORD_HEADER = 'x-authproxy-token-password'


class AuthProxyHTTPException(Exception):
    def __init__(self, response):
        self.response = response

    def __unicode__(self):
        return '{} {}'.format(self.response.status_code, self.response.content)

    __str__ = __unicode__

class AuthProxyClient(object):

    class ServerRouter(object):
        def __init__(self, url):
            self.url = _validate_server_url(url)

        def token_url(self, token):
            return self.url + '/{}'.format(token)

        def proxy_url(self, token, path):
            if not path.startswith('/'):
                raise ValueError('Path must include leading slash: {!r}'.format(path))
            return self.url + '/{}{}'.format(token, path)

    def __init__(self, server_url, get_password):
        """
        :param server_url: url for the AuthProxy server
        :param get_password: function that retrieves password given a token
        """
        self.router = self.ServerRouter(server_url)
        self.get_password = get_password

    def create_or_update_credential(self, token, target, auth=None):
        credential = Credential(target=target, auth=auth or NoneAuth())

        token_password = self.get_password(token)

        response = requests.put(self.router.token_url(token), json=credential.to_json(), headers={
            AUTH_PROXY_TOKEN_PASSWORD_HEADER: base64.b64encode(token_password)
        })

        if response.status_code != 201:
            raise AuthProxyHTTPException(response)

    def has_credential(self, token):
        response = requests.head(self.router.token_url(token))
        if response.status_code == 200:
            return True
        elif response.status_code == 404:
            return False
        else:
            raise AuthProxyHTTPException(response)

    def delete_credential(self, token):
        response = requests.delete(self.router.token_url(token))
        if response.status_code != 200:
            raise AuthProxyHTTPException(response)

    def requests(self, token):
        return ProxyingRequests(self, token)


class ProxyingRequests(object):
    def __init__(self, authproxy_client, token):
        self.authproxy_client = authproxy_client
        self.token = token

    def get_url(self, path):
        return self.authproxy_client.router.proxy_url(self.token, path)

    @property
    #todo: memoize
    def token_password(self):
        return self.authproxy_client.get_password(self.token)

    def _wrap_request(self, request_function, path, *args, **kwargs):
        headers = {header: value for header, value in kwargs.get('headers', {}).items()}
        headers[AUTH_PROXY_TOKEN_PASSWORD_HEADER] = base64.b64encode(self.token_password)
        kwargs['headers'] = headers
        return request_function(self.get_url(path), *args, **kwargs)

    def request(self, *args, **kwargs):
        return self._wrap_request(requests.request, *args, **kwargs)

    def get(self, *args, **kwargs):
        return self._wrap_request(requests.get, *args, **kwargs)

    def put(self, *args, **kwargs):
        return self._wrap_request(requests.put, *args, **kwargs)

    def post(self, *args, **kwargs):
        return self._wrap_request(requests.post, *args, **kwargs)

    def head(self, *args, **kwargs):
        return self._wrap_request(requests.head, *args, **kwargs)

    def delete(self, *args, **kwargs):
        return self._wrap_request(requests.delete, *args, **kwargs)


def _validate_server_url(url):
    parse_result = urlparse(url)
    if parse_result.scheme not in ('https', 'http'):
        raise ValueError('Server URL scheme must be https or http')
    elif not parse_result.netloc:
        raise ValueError('Server URL incomplete')
    elif parse_result.path or parse_result.params or parse_result.query or parse_result.fragment:
        raise ValueError('Server URL must be just the base location')
    return url
