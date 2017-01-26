import json
from django.db.models import Q
from django.http import StreamingHttpResponse, HttpResponse
from django.shortcuts import render
from openmrs.concepts.models import OpenmrsConcept
from openmrs.concepts.sync import openmrs_concept_json_from_api_json, \
    openmrs_concept_json_with_answers_from_concept
from openmrs.credentials.dbaccessors import get_credential
from openmrs.credentials.models import OpenmrsInstance
from openmrs.restclient.listapi import OpenmrsListApi


def all_openmrs_concepts(request, domain, credential_id):
    credential = get_credential(domain, int(credential_id))
    restclient = OpenmrsListApi(credential, 'concept')

    lines = (json.dumps(openmrs_concept_json_from_api_json(concept).to_json()) + '\n'
             for concept in restclient.get_all())
    return StreamingHttpResponse(lines, content_type='text/json')


def concept_search(request, domain):
    search = request.GET.get('q') or ''
    uuid = request.GET.get('uuid')
    instance = OpenmrsInstance.objects.get(domain=domain)
    if uuid:
        try:
            concept = OpenmrsConcept.objects.get(uuid=uuid, instance=instance)
        except OpenmrsConcept.DoesNotExist:
            return HttpResponse(json.dumps([]), content_type='text/json')
        else:
            return HttpResponse(
                json.dumps([
                    openmrs_concept_json_with_answers_from_concept(concept).to_json()
                ]), content_type='text/json')
    elif len(search) > 2:
        all_openmrs_concepts = OpenmrsConcept.objects.filter(Q(instance=instance) & ~Q(answers=None))
        openmrs_concepts = all_openmrs_concepts.filter(names__icontains=search)
        first_50 = openmrs_concepts[:50]
        return HttpResponse(
            json.dumps([
                openmrs_concept_json_with_answers_from_concept(concept).to_json()
                for concept in first_50
            ], content_type='text/json')
        )
    else:
        return HttpResponse(json.dumps([]), content_type='text/json')


def concept_search_page(request, domain):
    return render(request, 'openmrs/concepts/concept_search.html', {
        'domain': domain,
    })
