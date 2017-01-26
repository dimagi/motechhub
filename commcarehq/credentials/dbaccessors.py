from commcarehq.credentials.models import CommcarehqCredential


def get_credential(domain, credential_id):
    credential = CommcarehqCredential.objects.get(pk=credential_id)
    assert credential.instance.domain == domain
    return credential
