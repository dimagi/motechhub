from django.http import JsonResponse
from streams.models import Stream


def list_streams(request):
    return JsonResponse({
        'streams': [{'name': stream.name} for stream in Stream.objects.all()]
    })


def _create_stream(request, stream_name):
    if Stream.objects.exists(name=stream_name):
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


def _get_stream(request, stream_name):
    try:
        stream = Stream.objects.get(name=stream_name)
    except Stream.DoesNotExist:
        return JsonResponse({
            "error": "not_found",
            "reason": "The stream does not exist",
        }, status=404)
    else:
        return JsonResponse(
            {'name': stream.name},
            status=200
        )


def _delete_stream(request, stream_name):
    try:
        stream = Stream.objects.get(name=stream_name)
    except Stream.DoesNotExist:
        return JsonResponse({
            "error": "not_found",
            "reason": "The stream does not exist",
        }, status=404)
    else:
        stream.delete()
        return JsonResponse(
            {'name': stream.name},
            status=200
        )


def handle_stream(request, stream_name):
    if request.method == 'PUT':
        return _create_stream(request, stream_name)
    elif request.method == 'GET':
        return _get_stream(request, stream_name)
    elif request.method == 'DELETE':
        return _delete_stream(request, stream_name)
