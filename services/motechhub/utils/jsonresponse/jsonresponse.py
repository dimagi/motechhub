import json
from django.http import HttpResponse


def json_handler(obj):
    if callable(getattr(obj, 'to_json', None)):
        return obj.to_json()
    else:
        return json.JSONEncoder().default(obj)


def json_response(obj, status_code=200, **kwargs):
    if 'default' not in kwargs:
        kwargs['default'] = json_handler
    return HttpResponse(json.dumps(obj, **kwargs), status=status_code,
                        content_type="application/json")
