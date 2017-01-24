from openmrs.credentials.models import OpenmrsCredential


def get_credential(domain, credential_id):
    credential = OpenmrsCredential.objects.get(pk=credential_id)
    assert credential.instance.domain == domain
    return credential
