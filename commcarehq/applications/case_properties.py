from collections import defaultdict
from commcarehq.restclient.listapi import CommcarehqListApi
from utils.sorting.alphanumeric_sort import alphanumeric_sorted


def get_known_case_properties(credential):
    api = CommcarehqListApi(credential, 'application')
    properties_by_case_type = defaultdict(set)
    for app in api.get_all():
        for module in app['modules']:
            if module['case_type']:
                properties_by_case_type[module['case_type']].update(module['case_properties'])
    case_types = alphanumeric_sorted(properties_by_case_type)
    case_type_properties_pairs = []
    for case_type in case_types:
        case_type_properties_pairs.append((case_type, alphanumeric_sorted(properties_by_case_type[case_type])))
    return case_type_properties_pairs
