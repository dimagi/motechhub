from copy import deepcopy
import json
from django.http import StreamingHttpResponse
import itertools
from openmrs.credentials.dbaccessors import get_credential
from openmrs.restclient.listapi import OpenmrsListApi


def all_openmrs_concepts(request, domain, credential_id):
    credential = get_credential(domain, int(credential_id))
    restclient = OpenmrsListApi(credential, 'concept')

    all_keys = set()

    def format_concept(concept):
        formatted_concept = deepcopy(concept)
        formatted_concept['conceptClass'] = concept['conceptClass']['display']
        formatted_concept['datatype'] = concept['datatype']['display']
        formatted_concept['descriptions'] = [description['display']
                                             for description in concept['descriptions']]
        formatted_concept['names'] = [{'display': name['display'], 'locale': name['locale']}
                                      for name in concept['names']]
        formatted_concept['answers'] = [answer['uuid']
                                        for answer in concept['answers']]
        del formatted_concept['name']
        del formatted_concept['auditInfo']
        del formatted_concept['links']
        del formatted_concept['version']
        del formatted_concept['resourceVersion']
        del formatted_concept['mappings']
        del formatted_concept['setMembers']
        new_keys = set(formatted_concept.keys()) - all_keys
        if new_keys:
            print new_keys
        all_keys.update(formatted_concept.keys())
        return formatted_concept
    lines = (json.dumps(format_concept(concept)) + '\n'
             for concept in restclient.get_all())
    all_lines = itertools.chain(['[\n'], lines, [']\n'])
    return StreamingHttpResponse(
        all_lines,
        content_type='text/json'
    )
