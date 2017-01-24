import os
import pickle
import urllib
import requests


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


CACHE_DIR = 'cache'


class CachedRequests(object):

    def get_cache_filename(self, url, params):
        if params:
            url_with_params = url + '?' + urllib.urlencode(sorted(params.items()))
        else:
            url_with_params = url
        return os.path.join(CACHE_DIR, str(hash(url_with_params)))

    def get(self, url, *args, **kwargs):
        filename = self.get_cache_filename(url, kwargs.get('params'))
        print filename
        if os.path.exists(filename):
            with open(filename, 'r') as f:
                return pickle.load(f)

        print url, kwargs.get('params')
        value = requests.get(url, *args, **kwargs)
        with open(filename, 'w') as f:
            pickle.dump(value, f)
        return value


cached_requests = CachedRequests()
