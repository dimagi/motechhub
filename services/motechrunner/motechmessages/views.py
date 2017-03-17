import json
import uuid
from django.db import transaction
from django.http import JsonResponse
from django.views.decorators.http import require_POST, require_http_methods, require_GET
import jsonobject
import pytz
from jobs.dbaccessors import get_jobs_matching_message
from motechmessages.models import Message, MessageRun, MessageRunJob
from streams.view_decorators import require_valid_stream


@require_POST
@transaction.atomic
@require_valid_stream
def _post_message(request, stream):
    try:
        message_body = json.loads(request.body)
    except ValueError:
        return JsonResponse({
            'error': 'bad_request',
            'reason': 'request body must be valid JSON'
        }, status=400)

    message = Message(
        stream=stream,
        uuid=uuid.uuid4(),
        body=message_body,
    )
    message.save()

    message_run = MessageRun(message=message)
    message_run.save()

    jobs = get_jobs_matching_message(stream, message)
    for job in jobs:
        message_run_job = MessageRunJob(
            message_run=message_run,
            job=job,
            state='scheduled',
        )
        message_run_job.save()

    # todo: enqueue task to run each run job

    return JsonResponse({
        'ok': True,
        'id': str(message.uuid),
    }, status=201)


class MessageJSON(jsonobject.JsonObject):
    _allow_dynamic_properties = False
    _string_conversions = ()

    created = jsonobject.DateTimeProperty(exact=True)
    body = jsonobject.DictProperty()
    runs = jsonobject.ListProperty(lambda: MessageJSON.MessageRunJSON)

    class MessageRunJSON(jsonobject.JsonObject):

        created = jsonobject.DateTimeProperty(exact=True)
        run_jobs = jsonobject.ListProperty(
            lambda: MessageJSON.MessageRunJSON.MessageRunJobJSON,
            name='runJobs')

        class MessageRunJobJSON(jsonobject.JsonObject):
            job = jsonobject.ObjectProperty(lambda: MessageJSON.MessageRunJSON.MessageRunJobJSON.MessageRunJobInfoJSON)
            state = jsonobject.StringProperty()
            modified = jsonobject.DateTimeProperty()

            class MessageRunJobInfoJSON(jsonobject.JsonObject):
                id = jsonobject.StringProperty()
                rev = jsonobject.IntegerProperty()

    @classmethod
    def from_message(cls, message):
        return cls(
            created=message.created.astimezone(pytz.utc).replace(tzinfo=None),
            body=message.body,
            runs=[
                cls.MessageRunJSON(
                    created=message_run.created.astimezone(pytz.utc).replace(tzinfo=None),
                    run_jobs=[
                        cls.MessageRunJSON.MessageRunJobJSON(
                            job=cls.MessageRunJSON.MessageRunJobJSON.MessageRunJobInfoJSON(
                                id=str(message_run_job.job.uuid),
                                rev=message_run_job.job.rev,
                            ),
                            state=message_run_job.state,
                            modified=message_run_job.modified.astimezone(pytz.utc).replace(tzinfo=None)
                        )
                        for message_run_job in message_run.messagerunjob_set.all()
                    ]
                )
                for message_run in message.messagerun_set.all()
            ],
        )


@require_GET
@require_valid_stream
def _get_message_list(request, stream):
    try:
        limit = int(request.GET.get('limit'))
    except (TypeError, ValueError):
        return JsonResponse({
            'error': 'bad_request',
            'reason': 'The limit GET param is required and must be an integer.'
        }, status=400)

    messages = Message.objects.filter(stream=stream).order_by('-pk')[:limit]

    return JsonResponse([
        MessageJSON.from_message(message).to_json()
        for message in messages
    ], status=200, safe=False)


@require_http_methods(['GET', 'POST'])
def handle_messages(request, stream_name):
    if request.method == 'GET':
        return _get_message_list(request, stream_name)
    elif request.method == 'POST':
        return _post_message(request, stream_name)
