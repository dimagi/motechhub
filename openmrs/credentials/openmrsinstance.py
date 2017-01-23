from collections import namedtuple
import requests

ApiResponse = namedtuple('ApiResponse', 'result next_index')


class OpenmrsListApi(object):
    def __init__(self, credential, api_name):
        assert api_name in ['concept']
        self.instance = credential.instance
        self.credential = credential
        self.api_name = api_name

    def _get_next_start_index(self, next_url):
        before, after = next_url.split('?')
        start_index_literal, start_index = after.split('=')
        assert before == self._make_url()
        assert start_index_literal, 'startIndex'
        return int(start_index)

    def _make_url(self):
        """
        e.g. http://demo.openmrs.org/openmrs/ws/rest/v1/concept
        """
        return '{}/ws/rest/v1/{}'.format(self.instance.url, self.api_name)

    def get_list(self, start_index=0):
        response = requests.get(
            self._make_url(),
            data={'startIndex': start_index},
            auth=(self.credential.username, self.credential.password)
        ).json()
        next_url, = [link['uri'] for link in response['links']
                     if link['rel'] == 'next'] or [None]

        return ApiResponse(response['result'], self._get_next_start_index(next_url))

    def get_all(self):
        start_index = 0
        while start_index is not None:
            result, start_index = self.get_list(start_index)
            for obj in result:
                yield obj
