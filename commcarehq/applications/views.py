import json
from django.http import HttpResponse
from django.shortcuts import render
from commcarehq.applications.case_properties import get_known_case_properties
from commcarehq.credentials.models import CommcarehqInstance, CommcarehqCredential


def known_case_properties(request, domain):
    instance = CommcarehqInstance.objects.get(domain=domain)
    credential = CommcarehqCredential.objects.get(instance=instance)
    return HttpResponse(
        json.dumps([{'caseType': case_type, 'properties': properties}
                    for case_type, properties in get_known_case_properties(credential)]),
        content_type='text/json')


def known_case_properties_page(request, domain):
    return render(request, 'commcarehq/applications/search_properties.html', {
        'domain': domain,
    })
