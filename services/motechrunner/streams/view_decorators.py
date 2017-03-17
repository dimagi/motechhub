from functools import wraps
from django.http import JsonResponse
from streams.models import Stream


def require_valid_stream(fn):
    @wraps(fn)
    def inner(request, stream_name, *args, **kwargs):
        try:
            stream = Stream.objects.get(name=stream_name)
        except Stream.DoesNotExist:
            return JsonResponse({
                'error': 'not_found',
                'reason': "The stream does not exist."
            }, status=404)
        else:
            return fn(request, stream, *args, **kwargs)
    return inner
