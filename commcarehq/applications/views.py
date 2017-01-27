import json
from django.http import HttpResponse
from django.shortcuts import render
from commcarehq.applications.case_properties import get_known_case_properties
from commcarehq.applications.form_questions import get_applications, \
    get_application_forms, get_application_form_questions
from commcarehq.credentials.dbaccessors import get_credential_for_domain
from commcarehq.credentials.models import CommcarehqInstance, CommcarehqCredential
from utils.jsonresponse.jsonresponse import json_response


def applications(request, domain):
    credential = get_credential_for_domain(domain)
    return json_response(get_applications(credential))


def application_forms(request, domain, app_id):
    credential = get_credential_for_domain(domain)
    return json_response(get_application_forms(credential, app_id))


def application_form_questions(request, domain, app_id, form_id):
    credential = get_credential_for_domain(domain)
    return json_response(get_application_form_questions(credential, app_id, form_id))


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
