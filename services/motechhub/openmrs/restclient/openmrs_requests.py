from utils.restclient.cached_requests import cached_requests


class OpenmrsRequests(object):
    def __init__(self, credential):
        self.credential = credential
        self.requests = cached_requests

    def get(self, path, **params):
        return self.requests.get(
            '{}/{}'.format(self.credential.instance.url, path),
            auth=(self.credential.username, self.credential.password),
            **params
        )
