from commcarehq.credentials.models import CommcarehqCredential, CommcarehqInstance


def get_credential(domain, credential_id):
    credential = CommcarehqCredential.objects.get(pk=credential_id)
    assert credential.instance.domain == domain
    return credential


def get_credential_for_domain(domain):
    instance = CommcarehqInstance.objects.get(domain=domain)
    return CommcarehqCredential.objects.get(instance=instance)
