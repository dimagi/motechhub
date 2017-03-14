from openmrs.credentials.models import OpenmrsCredential, OpenmrsInstance


def get_credential(domain, credential_id):
    credential = OpenmrsCredential.objects.get(pk=credential_id)
    assert credential.instance.domain == domain
    return credential


def get_credential_for_domain(domain):
    instance = OpenmrsInstance.objects.get(domain=domain)
    return OpenmrsCredential.objects.get(instance=instance)
