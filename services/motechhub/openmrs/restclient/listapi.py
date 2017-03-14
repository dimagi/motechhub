from urlparse import urlparse, parse_qs

from openmrs.restclient.openmrs_requests import OpenmrsRequests

from utils.restclient.listapi import ListApi, ApiResponse


class OpenmrsListApi(ListApi):
    def __init__(self, credential, api_name):
        assert api_name in ['concept', 'patientidentifiertype']
        self.instance = credential.instance
        self.credential = credential
        self.api_name = api_name
        self.requests = OpenmrsRequests(credential)

    def _get_next_start_index(self, next_url):
        parsed_url = urlparse(next_url)
        query_params = parse_qs(parsed_url.query)
        assert parsed_url._replace(query='').geturl() == '{}/{}'.format(self.instance.url, self._make_url())
        assert set(query_params.keys()) == {'startIndex', 'v'}
        start_index, = query_params['startIndex']
        return int(start_index)

    def _make_url(self):
        """
        e.g. http://demo.openmrs.org/openmrs/ws/rest/v1/concept
        """
        return 'ws/rest/v1/{}'.format(self.api_name)

    def get_list(self, start_index=0):
        response = self.requests.get(
            self._make_url(),
            params={'startIndex': start_index, 'v': 'full'},
        ).json()
        next_url, = [link['uri'] for link in response.get('links', [])
                     if link['rel'] == 'next'] or [None]
        if next_url:
            return ApiResponse(response['results'], self._get_next_start_index(next_url))
        else:
            return ApiResponse(response['results'], None)
