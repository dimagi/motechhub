from utils.restclient.cached_requests import cached_requests


class CommcarehqRequests(object):
    def __init__(self, credential):
        self.credential = credential
        self.requests = cached_requests

    def get(self, path, **params):
        url = '{}/a/{}/{}'.format(self.credential.instance.url,
                                self.credential.instance.commcarehq_domain, path)
        headers = {'Authorization': 'ApiKey {}:{}'.format(self.credential.username,
                                                          self.credential.api_key)}
        return self.requests.get(url, headers=headers, **params)
