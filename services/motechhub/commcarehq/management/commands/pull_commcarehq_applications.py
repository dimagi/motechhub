from collections import defaultdict
from django.core.management import BaseCommand
from commcarehq.credentials.dbaccessors import get_credential
from commcarehq.restclient.listapi import CommcarehqListApi


class Command(BaseCommand):
    def handle(self, *args, **options):
        credential = get_credential('droberts', 1)
        api = CommcarehqListApi(credential, 'application')
        case_types = defaultdict(list)
        for app in api.get_all():
            print app['id']
            for module in app['modules']:
                if module['case_type']:
                    case_types[module['case_type']].extend(module['case_properties'])
        print case_types
