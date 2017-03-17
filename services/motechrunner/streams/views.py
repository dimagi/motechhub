from django.http import JsonResponse
from streams.models import Stream
from streams.view_decorators import require_valid_stream


def list_streams(request):
    return JsonResponse({
        'streams': [{'name': stream.name} for stream in Stream.objects.all()]
    })


def _create_stream(request, stream_name):
    if Stream.objects.filter(name=stream_name).exists():
        return JsonResponse({
            "error": "file_exists",
            "reason": "The stream could not be created, the file already exists."
        }, status=412)
    else:
        stream = Stream(name=stream_name)
        stream.save()
        return JsonResponse(
            {'ok': True},
            status=201
        )


@require_valid_stream
def _get_stream(request, stream):
    return JsonResponse(
        {'name': stream.name},
        status=200
    )


@require_valid_stream
def _delete_stream(request, stream):
    stream.delete()
    return JsonResponse(
        {'ok': True},
        status=200
    )


def handle_stream(request, stream_name):
    if request.method == 'PUT':
        return _create_stream(request, stream_name)
    elif request.method == 'GET':
        return _get_stream(request, stream_name)
    elif request.method == 'DELETE':
        return _delete_stream(request, stream_name)
