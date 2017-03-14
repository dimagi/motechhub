from urlparse import parse_qs
from commcarehq.restclient.commcarehq_requests import CommcarehqRequests
from utils.restclient.listapi import ListApi, ApiResponse


class CommcarehqListApi(ListApi):
    def __init__(self, credential, api_name):
        assert api_name in ['application']
        self.instance = credential.instance
        self.credential = credential
        self.api_name = api_name
        self.requests = CommcarehqRequests(credential)
        self.limit = {'application': 4}[api_name]

    def _get_next_start_index(self, next_params):
        assert next_params.startswith('?')
        query_params = parse_qs(next_params[1:])
        assert set(query_params.keys()) == {'offset', 'limit', 'format'}
        start_index, = query_params['offset']
        return int(start_index)

    def _make_url(self):
        """
        e.g. https://demo.commcarehq.org/a/example/api/v0.5/application/
        """
        return 'api/v0.5/{}/'.format(self.api_name)

    def get_list(self, start_index=0):
        response = self.requests.get(
            self._make_url(),
            params={'offset': start_index, 'format': 'json', 'limit': self.limit},
        )
        if response.status_code != 200:
            raise Exception(response)
        response = response.json()
        next_params = response['meta']['next']
        if next_params:
            return ApiResponse(response['objects'], self._get_next_start_index(next_params))
        else:
            return ApiResponse(response['objects'], None)
