import json
import uuid
from django.db import IntegrityError
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods, require_GET
import jsonobject
from jsonobject.exceptions import WrappingAttributeError, BadValueError
from jobs.models import Job
from streams.models import Stream


class _PutJobBody(jsonobject.JsonObject):
    _allow_dynamic_properties = False
    javascript = jsonobject.StringProperty(required=True)
    filter = jsonobject.DictProperty()
    # the rev of the job to _replace_; value of 0 means create
    rev = jsonobject.IntegerProperty(default=0, validators=lambda rev: rev >= 0)


def _get_job(request, stream_name, job_id):
    try:
        job = Job.objects.filter(uuid=job_id, stream__name=stream_name).order_by('-rev')[0]
    except (Stream.DoesNotExist, IndexError):
        return JsonResponse({
            'error': 'not_found',
            'reason': "The job does not exist."
        }, status=404)
    else:
        return JsonResponse({
            'id': str(job.uuid),
            'rev': job.rev,
            'filter': job.filter,
            'javascript': job.javascript,
        })


def _put_job(request, stream_name, job_id):
    try:
        stream = Stream.objects.get(name=stream_name)
    except Stream.DoesNotExist:
        return JsonResponse({
            'error': 'not_found',
            'reason': "The stream does not exist."
        }, status=404)

    try:
        job_spec = json.loads(request.body)
    except ValueError:
        return JsonResponse({
            'error': 'bad_request',
            'reason': 'request body must be valid JSON'
        }, status=400)

    try:
        job_spec = _PutJobBody.wrap(job_spec)
    except (WrappingAttributeError, BadValueError):
        return JsonResponse({
            'error': 'bad_request',
            'reason': 'Request body JSON must adhere to spec'
        }, status=400)

    def update_conflict_response():
        return JsonResponse({
            'error': 'conflict',
            'reason': 'The rev must match the rev of the last update to this job.'
        }, status=409)

    if job_spec.rev > 0:
        if not Job.objects.filter(uuid=job_id, rev=job_spec.rev).exists():
            return update_conflict_response()

    job = Job(
        uuid=uuid.UUID(job_id),
        rev=job_spec.rev + 1,
        filter=job_spec.filter,
        javascript=job_spec.javascript,
        stream=stream,
    )

    try:
        job.save()
    except IntegrityError:
        # (uuid, rev) is not unique)
        return update_conflict_response()

    return JsonResponse({
        'ok': True,
        'id': job.uuid,
        'rev': job.rev,
    }, status=201)


@require_http_methods(['PUT', 'GET'])
def handle_job(request, stream_name, job_id):
    if request.method == 'PUT':
        return _put_job(request, stream_name, job_id)
    elif request.method == 'GET':
        return _get_job(request, stream_name, job_id)


@require_GET
def get_job_list(request, stream_name):
    try:
        stream = Stream.objects.get(name=stream_name)
    except Stream.DoesNotExist:
        return JsonResponse({
            'error': 'not_found',
            'reason': "The stream does not exist."
        }, status=404)

    jobs = Job.get_latest_jobs(stream)
    return JsonResponse([{
        'id': str(job.uuid),
        'rev': job.rev,
        'filter': job.filter,
        'javascript': job.javascript,
    } for job in jobs], safe=False)
