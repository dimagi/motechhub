import json
import uuid
from django.db import transaction
from django.http import JsonResponse
from django.views.decorators.http import require_POST, require_http_methods, require_GET
import jsonobject
import pytz
from motechmessages.models import Message, MessageRun
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

    # todo: create runs jobs for each matching job

    return JsonResponse({
        'ok': True,
        'id': str(message.uuid),
    }, status=201)


class MessageJSON(jsonobject.JsonObject):
    _allow_dynamic_properties = False
    _string_conversions = ()

    created = jsonobject.DateTimeProperty(exact=True)
    body = jsonobject.DictProperty()

    @classmethod
    def from_message(cls, message):
        return cls(
            created=message.created.astimezone(pytz.utc).replace(tzinfo=None),
            body=message.body,
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
