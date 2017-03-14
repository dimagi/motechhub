from django.core.management import BaseCommand
from openmrs.concepts.sync import sync_concepts_from_openmrs
from openmrs.credentials.dbaccessors import get_credential


class Command(BaseCommand):
    def handle(self, *args, **options):
        credential = get_credential('droberts', 1)
        sync_concepts_from_openmrs(credential)
